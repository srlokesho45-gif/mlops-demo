
pipeline {
    agent any

    stages {
        stage('Check Tools') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage('Code Quality Check') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -r requirements-dev.txt'
                sh '.venv/bin/ruff check train.py test_model.py'
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

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mlops-demo:v1 .'
            }
        }

        stage('Test Docker Container') {
            steps {
                sh 'docker run --rm mlops-demo:v1'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: ML tests and Docker pipeline completed!'
        }
        failure {
            echo 'FAILED: Check Console Output.'
        }
    }
}
