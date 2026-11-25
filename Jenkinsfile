pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run tests in')
    }

    environment {
        // Keep Playwright browsers inside the workspace so the Jenkins service user can find them
        PLAYWRIGHT_BROWSERS_PATH = "${WORKSPACE}\\ms-playwright"
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python env') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install %BROWSER%
                '''
            }
        }

        stage('Run tests') {
            steps {
                // Don't fail the pipeline here; Allure + JUnit mark the build UNSTABLE on test failures
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
