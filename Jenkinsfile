
pipeline {
  agent {
    docker {
      image 'python:3.11-slim'
    }
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    PYTHONUNBUFFERED = '1'
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PIP_NO_CACHE_DIR = '1'
    SKIP_DB = '1'

    GITHUB_OWNER      = 'Abhinash0702'
    GITHUB_REPO       = 'DevOps_CaseStudy'
    GITHUB_TOKEN_CRED = 'jenkins-github-access'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Env') {
      steps {
        dir('app') {
          sh '''
            set -e
            python --version
            python -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            if [ -f requirements.txt ]; then
              pip install -r requirements.txt
            else
              pip install Flask mysql-connector-python
            fi
            pip install pytest
          '''
        }
      }
    }

    stage('Run Tests') {
      steps {
        dir('app') {
          sh '''
            set -e
            . venv/bin/activate
            pytest --maxfail=1 --disable-warnings -q
          '''
        }
      }
    }

    stage('Approval (PR only)') {
      when { expression { return env.CHANGE_ID } }
      steps {
        input message: "Approve merging PR #${env.CHANGE_ID} into ${env.CHANGE_TARGET}?",
              ok: "Approve & Merge"
      }
    }
  }  // ✅ CLOSE stages block here

  post {
    success {
      echo '✅ Python code validated successfully.'
      
     echo '✅ Merge successful. Triggering deployment job...'
    build job: 'Deploy-CaseStudy', wait: false

    }
    failure {
      echo '❌ Validation failed. Check the stage logs above.'
    }
    always {
      script {
        try {
          cleanWs()
        } catch (e) {
          echo "Skipping cleanWs(): ${e}"
        }
      }
    }
  }
}
