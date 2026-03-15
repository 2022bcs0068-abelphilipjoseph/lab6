pipeline {
    agent any

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
                    python3 -m venv venv
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
                    // Builds the image tagged with the Jenkins build number
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image (Conditional)') {
            when {
                environment name: 'DEPLOY_MODEL', value: 'true'
            }
            steps {
                script {
                    // Authenticates and pushes to Docker Hub
                    docker.withRegistry('', 'dockerhub-creds') {
                        dockerImage.push("${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
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
