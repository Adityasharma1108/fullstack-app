pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME   = "adityadocker10"
        IMAGE_NAME            = "fullstack-todo-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds"
        IMAGE_TAG              = "${env.BUILD_NUMBER}"
        FULL_IMAGE              = "${DOCKERHUB_USERNAME}/${IMAGE_NAME}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Checking out source code from repository..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${FULL_IMAGE}:${IMAGE_TAG}"
                sh "docker build -t ${FULL_IMAGE}:${IMAGE_TAG} -t ${FULL_IMAGE}:latest ."
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo "Logging into Docker Hub..."
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDENTIALS_ID}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub: ${FULL_IMAGE}"
                sh "docker push ${FULL_IMAGE}:${IMAGE_TAG}"
                sh "docker push ${FULL_IMAGE}:latest"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded! Image pushed: ${FULL_IMAGE}:${IMAGE_TAG}"
        }
        failure {
            echo "❌ Pipeline failed. Check the logs above for details."
        }
        always {
            sh 'docker logout || true'
        }
    }
}