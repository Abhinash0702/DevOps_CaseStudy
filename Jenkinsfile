
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                  python3 -m venv venv
                  . venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                  pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                  . venv/bin/activate
                  pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Python code validated successfully!"
        }
        failure {
            echo "❌ Validation failed. Check logs for details."
        }
    }
}

