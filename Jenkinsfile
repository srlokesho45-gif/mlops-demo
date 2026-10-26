
pipeline {
    agent any

    stages {
        stage('Check Tools') {
            steps {
                sh 'python3 --version'
                sh 'docker --version'
            }
        }

        stage('Code Quality Check') {
            steps {
                sh '.venv/bin/ruff check train.py test_model.py evaluate_model.py test_evaluation.py compare_experiments.py test_compare_experiments.py app.py test_api.py'
            }
        }

        stage('Validate Model Metadata') {
            steps {
                sh 'python3 -m json.tool model_version.json'
            }
        }
         
        stage('Test Prediction API') {
            steps {
                   sh 'python3 -m venv .venv-api'
                   sh '.venv-api/bin/pip install -r requirements-api.txt'
                   sh '.venv-api/bin/python -m unittest -v test_api.py'
 
                  }
                  }


       stage('Version Model') {
    steps {
        sh 'python3 version_model.py'
        sh 'python3 -m unittest -v test_version_model.py'
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

        
       stage('Validate Model Release') {
           steps {
               sh 'python3 validate_release.py'
               sh 'python3 -m unittest -v test_validate_release.py'
            }
        }

       stage('Build Docker Image') {
           steps {
                 sh 'docker build -t mlops-demo:v4 .'
            }
        }

       stage('Verify Model Metadata in Docker') {
           steps {
                 sh 'docker run --rm --entrypoint cat mlops-demo:v4 /app/model_version.json'
            }
         }

        
stage('Test Docker Container') {
    steps {
        sh '''
            set -eu
            docker rm -f mlops-api-test >/dev/null 2>&1 || true
            trap 'docker rm -f mlops-api-test >/dev/null 2>&1 || true' EXIT

            docker run -d --name mlops-api-test \
                -p 18000:8000 mlops-demo:v4

            ready=0
            for attempt in $(seq 1 20); do
                if curl -fsS http://localhost:18000/health >/dev/null; then
                    ready=1
                    break
                fi
                sleep 1
            done

            test "$ready" -eq 1

            curl -fsS -X POST http://localhost:18000/predict \
                -H 'Content-Type: application/json' \
                -d '{"study_hours":5}' |
                python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["predicted_marks"] == 60.0, d; print("Docker API prediction passed:", d)'
        '''
    }
}

    post {
        success {
            archiveArtifacts artifacts: 'model.json,model_version.json,metrics.json,experiments.jsonl,experiment_report.json', fingerprint: true
            echo 'SUCCESS: MLOps pipeline, evaluation, and experiment tracking completed!'
        }

        failure {
            echo 'FAILED: Check Console Output.'
        }
    }
}
