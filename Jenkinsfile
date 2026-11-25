pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run tests in')
    }

    environment {
        // Keep Playwright browsers inside the workspace so the Jenkins service user can find them
        PLAYWRIGHT_BROWSERS_PATH = "${WORKSPACE}\\ms-playwright"
        PYTHONUNBUFFERED = '1'
        // Fallback in case the parameter isn't set (e.g. very first build)
        BROWSER = "${params.BROWSER ?: 'chromium'}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Downloads the project (tests, requirements.txt, pytest.ini) into the workspace.
                // Works both for "Pipeline script" and "Pipeline script from SCM" jobs.
                git url: 'https://github.com/Lukameladz3/Python-Jenkins-Allure.git', branch: 'main'
            }
        }

        stage('Setup Python env') {
            steps {
                // "if errorlevel 1 exit /b 1" makes the stage fail immediately if a command fails
                bat '''
                    python -m venv venv
                    if errorlevel 1 exit /b 1
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    if errorlevel 1 exit /b 1
                    playwright install %BROWSER%
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Run tests') {
            steps {
                // Don't fail the pipeline here; JUnit + Allure mark the build UNSTABLE on test failures
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        pytest --browser %BROWSER% --junitxml=test-results\\junit.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results/junit.xml'
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]
        }
    }
}
