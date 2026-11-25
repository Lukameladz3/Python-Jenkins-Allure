# Python + Playwright + Jenkins + Allure

Simple UI tests written with **pytest + Playwright**, run by **Jenkins** (locally on Windows) with an **Allure** report.

## Project structure

```
├── Jenkinsfile                  # Jenkins pipeline (Windows "bat" steps)
├── pytest.ini                   # pytest config (writes Allure results to allure-results/)
├── requirements.txt
└── tests/
    ├── conftest.py              # attaches a screenshot to Allure when a test fails
    ├── test_login.py            # saucedemo.com login tests
    └── test_playwright_site.py  # playwright.dev tests
```

## Run tests locally (without Jenkins)

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                    # headless
pytest --headed           # see the browser
pytest --browser firefox  # other browser (run `playwright install firefox` first)
```

To view the Allure report locally you need the Allure CLI (`scoop install allure`, needs Java):

```powershell
allure serve allure-results
```

---

## Jenkins setup, step by step (Windows)

### 1. Requirements
- **Java 17 or 21** – check with `java -version`.
- **Python 3.10+** on PATH – check with `python --version`.
- **Git** – check with `git --version`.

### 2. Install and start Jenkins
The easiest way locally is to run the WAR file as your own user, so Jenkins sees your Python and Git:

1. Download the **Generic Java package (.war)** (LTS) from https://www.jenkins.io/download/
2. Put it in a folder, e.g. `C:\jenkins\jenkins.war`
3. Start it:
   ```powershell
   cd C:\jenkins
   java -jar jenkins.war --httpPort=8080
   ```
4. Open http://localhost:8080

> If you use the Windows **MSI installer** instead, Jenkins runs as a Windows service under a different user.
> Then Python may not be found: install Python "for all users" and add it to the system PATH, or set PATH under
> *Manage Jenkins → System → Global properties → Environment variables*.

### 3. Unlock Jenkins
1. Copy the initial admin password printed in the console (also in `C:\Users\<you>\.jenkins\secrets\initialAdminPassword`).
2. Paste it into the browser.
3. Choose **Install suggested plugins** (this includes Pipeline, Git and JUnit).
4. Create your admin user and keep the URL `http://localhost:8080/`.

### 4. Install the Allure plugin
1. **Manage Jenkins → Plugins → Available plugins**
2. Search for **Allure** and install **Allure Jenkins Plugin**
3. Restart Jenkins if it asks.

### 5. Configure the Allure command-line tool
1. **Manage Jenkins → Tools**
2. Scroll to **Allure Commandline installations → Add Allure Commandline**
3. Name: `allure`
4. Tick **Install automatically** → *From Maven Central* → pick the latest version
5. **Save**

### 6. Create the pipeline job
1. Dashboard → **New Item**
2. Name: `python-playwright-allure`, type **Pipeline** → **OK**
3. In **Pipeline** section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: your GitHub repo URL, e.g. `https://github.com/<user>/Python-Jenkins-Allure.git`
     (for a private repo, add credentials: username + GitHub personal access token)
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
4. **Save**

> **Using a local folder instead of GitHub:** Jenkins blocks local `file://` repos by default.
> Start Jenkins with
> `java -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true -jar jenkins.war --httpPort=8080`
> and use `file:///C:/Users/<you>/Desktop/Python-Jenkins-Allure` as the Repository URL
> (only committed changes are picked up).

### 7. Run the job
1. Open the job → **Build Now**.
   (After the first run the button becomes **Build with Parameters**, where you can pick the browser.)
2. The pipeline will:
   - check out the code
   - create a virtualenv and install requirements + the Playwright browser
   - run pytest
   - publish JUnit results and the Allure report

### 8. Open the Allure report
- On the job page or build page click **Allure Report** (left menu or the Allure icon).
- You'll see the features, steps for each test, and a screenshot attached for any failing test.
- After a few builds the **Trend** graph shows history.

### Build result meaning
- **Green (SUCCESS)** – all tests passed
- **Yellow (UNSTABLE)** – some tests failed, report is still generated
- **Red (FAILURE)** – something broke before/outside tests (e.g. pip install failed)

## Troubleshooting
| Problem | Fix |
|---|---|
| `'python' is not recognized` | Python is not on the PATH of the user running Jenkins (see step 2 note). |
| `Executable doesn't exist ... ms-playwright` | The `playwright install` step didn't run / failed – check the *Setup Python env* stage log. |
| No "Allure Report" link | Allure plugin not installed or no Allure Commandline configured (steps 4–5). |
| Allure report is empty | Check that `allure-results/` is created in the workspace after the *Run tests* stage. |
