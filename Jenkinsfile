
pipeline {
  agent {
    docker {
      image 'python:3.11-alpine'   // or 'python:3.11-slim' if you need glibc / build tools
      args  '-u'                   // unbuffered stdout for clearer logs
    }
  }

  options {
    timestamps()
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PIP_NO_CACHE_DIR = '1'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Env') {
      steps {
        dir('app') {                 // adjust if your code/Jenkinsfile isn't under app/
          sh '''
            python --version
            python -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            if [ -f requirements.txt ]; then
              pip install -r requirements.txt
            fi
          '''
        }
      }
    }

    stage('Run Tests (skip DB)') {
      steps {
        dir('app') {
          sh '''
            . venv/bin/activate
            # Adjust command as needed; using pytest as an example
            if [ -f pytest.ini ] || [ -d tests ]; then
              pytest -q
            else
              python -m unittest discover -v
            fi
          '''
        }
      }
    }
  }

  post {
    success {
      echo '✅ Validation passed.'
    }
    failure {
      echo '❌ Validation failed. Check the stage logs above.'
    }
    always {
      cleanWs()
    }
  }
}

