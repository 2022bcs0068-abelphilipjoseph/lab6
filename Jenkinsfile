pipeline {
    agent any

    tools {
        dockerTool 'docker' 
    }

    environment {
        // Fetch the baseline accuracy from Jenkins credentials
        BEST_ACCURACY_CRED = credentials('best-accuracy')
        // UPDATE THIS to your actual Docker Hub username and repo name (e.g., 'iiitkabel/lab6-model')
        DOCKER_HUB_REPO = "iiitkabel/jenkins_automation_wine_prediction" 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    virtualenv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    # Adjust 'scripts/train.py' if your training script has a different name/path
                    python scripts/train.py 
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    // Uses 'jq' to extract the accuracy from the JSON file
                    // Ensure the key in metrics.json matches  '.r2_score' accordingly
                    env.CURRENT_ACCURACY = sh(script: "jq -r '.r2_score' app/artifacts/metrics.json", returnStdout: true).trim()
                    echo "Current Model Accuracy: ${env.CURRENT_ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    echo "Baseline Best Accuracy: ${env.BEST_ACCURACY_CRED}"
                    
                    // Convert strings to floats for comparison
                    if (env.CURRENT_ACCURACY.toFloat() > env.BEST_ACCURACY_CRED.toFloat()) {
                        echo "New model is better! Proceeding to build and push."
                        env.DEPLOY_MODEL = 'true'
                    } else {
                        echo "Model did not improve. Skipping deployment."
                        env.DEPLOY_MODEL = 'false'
                    }
                }
            }
        }

        stage('Build Docker Image (Conditional)') {
            when {
                environment name: 'DEPLOY_MODEL', value: 'true'
            }
            steps {
                script {
                    docker.withTool('docker'){
			sh 'docker build -t "$JD_IMAGE" . '
                }
            }
        }

        stage('Push Docker Image (Conditional)') {
            when {
                environment name: 'DEPLOY_MODEL', value: 'true'
            }
            steps {
                script {
                    
                    docker.withTool('docker') {
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        sh 'docker push "$JD_IMAGE" '
                    }
                }
            }
        }
    }

    // Task 5: Artifact Archiving
    post {
        always {
            // Archives everything in app/artifacts/ regardless of pass/fail
            archiveArtifacts artifacts: 'app/artifacts/**', allowEmptyArchive: true
        }
    }
}
