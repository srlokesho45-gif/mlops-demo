
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is available in the workspace'
            }
        }

        stage('Check Tools') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
            }
        }

        stage('Train ML Model') {
            steps {
                sh 'python3 train.py'
            }
        }

        stage('Test ML Model') {
            steps {
                sh 'python3 test_model.py'
            }
        }
    }
stage('Code Quality Check') {
    steps {
        sh 'python3 -m venv .venv'
        sh '.venv/bin/python -m pip install -r requirements-dev.txt'
        sh '.venv/bin/ruff check train.py test_model.py'
    }
}

    post {
        success {
            echo 'SUCCESS: AI/ML pipeline completed!'
        }
        failure {
            echo 'FAILED: Check Console Output.'
        }
    }
}
