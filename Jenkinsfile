
pipeline {
  agent {
    docker {
      image 'python:3.11-slim'      // keep your Python Docker agent
      // args '<docker run args>'   // leave empty unless you need extra Docker args
    }
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    // --- Your existing CI env ---
    PYTHONUNBUFFERED = '1'
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PIP_NO_CACHE_DIR = '1'
    SKIP_DB = '1'

    // --- Add these 3 for PR auto-merge (GitHub) ---
    GITHUB_OWNER      = 'Abhinash0702'   // e.g., 'abhinash' or your GitHub org
    GITHUB_REPO       = 'DevOps_CaseStudy'          // e.g., 'my-app'
    GITHUB_TOKEN_CRED = 'jenkins-github-access' // Jenkins credential ID (Secret text)
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

    stage('Run Tests (skip DB)') {
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

    // === New: Manual approval only for PR builds ===
    stage('Approval (PR only)') {
      when { expression { return env.CHANGE_ID } } // only for Pull Request builds in Multibranch
      steps {
        input message: "Approve merging PR #${env.CHANGE_ID} into ${env.CHANGE_TARGET}?",
              ok: "Approve & Merge"
              // Optionally restrict who can approve:
              // submitter: 'your-jenkins-username'
      }
    }

    // === New: Auto-merge PR after approval ===
    stage('Merge PR (PR only)') {
      when { expression { return env.CHANGE_ID } }
      steps {
        withCredentials([string(credentialsId: env.GITHUB_TOKEN_CRED, variable: 'GITHUB_TOKEN')]) {
          sh '''
            set -e

            PR_NUMBER=''' + '${CHANGE_ID}' + '''
            TARGET_BRANCH=''' + '${CHANGE_TARGET}' + '''     # usually "main"
            MERGE_METHOD="merge"                             # or "squash" / "rebase"

            echo "[Merge] Attempting to merge PR #${PR_NUMBER} into ${TARGET_BRANCH} (method: ${MERGE_METHOD})"

            # Call GitHub API to merge the PR
            curl -sS -X PUT \
              -H "Authorization: Bearer ${GITHUB_TOKEN}" \
              -H "Accept: application/vnd.github+json" \
              https://api.github.com/repos/''' + '${GITHUB_OWNER}/${GITHUB_REPO}' + '''/pulls/${PR_NUMBER}/merge \
              -d "{\"merge_method\":\"${MERGE_METHOD}\", \"commit_title\":\"CI merge PR #${PR_NUMBER}\"}" \
              | tee merge_result.json

            # Validate success without jq
            if grep -q '"merged": true' merge_result.json; then
              echo "[Merge] PR merged successfully."
            else
              echo "------ GitHub API response ------"
              cat merge_result.json
              echo "---------------------------------"
              echo "[Merge] Merge failed (conflicts, up-to-date requirement, or policy)."
              exit 1
            fi
          '''
        }
      }
    }
  }

  post {
    success {
      echo '✅ Python code validated successfully (DB skipped in CI).'
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
