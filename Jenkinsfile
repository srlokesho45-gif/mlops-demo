
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
                sh '.venv/bin/ruff check train.py test_model.py evaluate_model.py test_evaluation.py'
            }
        }

        stage('Validate Model Metadata') {
            steps {
                sh 'python3 -m json.tool model_version.json'
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

        stage('Evaluate Model') {
            steps {
                sh 'python3 evaluate_model.py'
                sh 'python3 -m json.tool metrics.json'
            }
        }

        stage('Test Evaluation') {
            steps {
                sh 'python3 -m unittest -v test_evaluation.py'
            }
        }

stage('Compare Experiments') {
    steps {
        sh 'python3 compare_experiments.py'
        sh 'python3 -m unittest -v test_compare_experiments.py'
    }
}


        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mlops-demo:v3 .'
            }
        }

        stage('Verify Model Metadata in Docker') {
            steps {
                sh 'docker run --rm --entrypoint cat mlops-demo:v3 /app/model_version.json'
            }
        }

        stage('Test Docker Container') {
            steps {
                sh 'docker run --rm mlops-demo:v3'
            }
        }
    }

    post {
    success {
        archiveArtifacts artifacts: 'model.json,model_version.json,metrics.json,experiments.jsonl', fingerprint: true
        echo 'SUCCESS: MLOps pipeline completed!'
    }
    failure {
        echo 'FAILED: Check Console Output.'
    }
}

