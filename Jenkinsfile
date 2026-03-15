pipeline {
    agent any
    
    // We keep our Docker tool configuration to prevent the "docker: not found" error!
    tools {
        dockerTool 'docker'
    }

    environment {
        // Ultimate PATH fix to ensure the shell finds the Docker tool
        PATH = "${tool 'docker'}/bin:${env.PATH}"
        
        VENV_DIR = "venv"
        METRICS_FILE = "app/artifacts/metrics.json"
        
        // YOUR Docker Hub Repository
        DOCKER_HUB_REPO = "iiitkabel/jenkins_automation_wine_prediction"
    }

    stages {
        // =========================
        // Stage 1: Checkout
        // =========================
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // =========================
        // Stage 2: Setup Python Virtual Environment
        // =========================
        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                vitualenv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // =========================
        // Stage 3: Train Model
        // =========================
        stage('Train Model') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python scripts/train.py
                '''
            }
        }

        // =========================
        // Stage 4: Read R2 and MSE
        // =========================
        stage('Read R2 and MSE') {
            steps {
                script {
                    // Requires the "Pipeline Utility Steps" plugin in Jenkins
                    def metrics = readJSON file: "${METRICS_FILE}"
                    env.CUR_R2 = metrics.r2_score.toString()
                    env.CUR_MSE = metrics.mse.toString()
                    echo "--------------------------------"
                    echo "Model Evaluation Metrics"
                    echo "R2 Score : ${env.CUR_R2}"
                    echo "MSE : ${env.CUR_MSE}"
                    echo "--------------------------------"
                }
            }
        }

        // =========================
        // Stage 5: Compare R2 and MSE
        // =========================
        stage('Compare R2 and MSE') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'BEST_R2', variable: 'BEST_R2_VAL'),
                        string(credentialsId: 'BEST_MSE', variable: 'BEST_MSE_VAL')
                    ]) {
                        def curR2 = env.CUR_R2.toFloat()
                        def curMSE = env.CUR_MSE.toFloat()
                        def bestR2 = BEST_R2_VAL.toFloat()
                        def bestMSE = BEST_MSE_VAL.toFloat()
                        
                        echo "Comparing model performance..."
                        
                        // Condition to deploy: Better R2 AND Better MSE
                        if (curR2 > bestR2 && curMSE < bestMSE) {
                            env.BUILD_DOCKER = "true"
                            echo "Model improved (Higher R2 & Lower MSE). Docker build will proceed."
                        } else {
                            env.BUILD_DOCKER = "false"
                            echo "Model NOT improved. Skipping Docker build."
                        }
                    }
                }
            }
        }

        // =========================
        // Stage 6: Build Docker Image
        // =========================
        stage('Build Docker Image') {
            when {
                expression { env.BUILD_DOCKER == "true" }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    // Using double quotes """ allows us to safely inject variables
                    sh """
                    echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                    docker build -t ${DOCKER_HUB_REPO}:${BUILD_NUMBER} .
                    docker tag ${DOCKER_HUB_REPO}:${BUILD_NUMBER} ${DOCKER_HUB_REPO}:latest
                    """
                }
            }
        }

        // =========================
        // Stage 7: Push Docker Image
        // =========================
        stage('Push Docker Image') {
            when {
                expression { env.BUILD_DOCKER == "true" }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    docker push ${DOCKER_HUB_REPO}:${BUILD_NUMBER}
                    docker push ${DOCKER_HUB_REPO}:latest
                    """
                }
            }
        }
    }

    // =========================
    // Artifact Archiving
    // =========================
    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}
