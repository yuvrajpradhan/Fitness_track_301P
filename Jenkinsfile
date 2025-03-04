pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/yuvrajpradhan/Fitness_track_301P' // Change this to your repo URL
            }
        }

        stage('Build and Start Containers') {
            steps {
                script {
                    sh 'docker-compose down' // Stop running containers (if any)
                    sh 'docker-compose build' // Build images
                    sh 'docker-compose up -d' // Start containers in detached mode
                }
            }
        }

        stage('Post Deployment Check') {
            steps {
                script {
                    sh 'docker ps' // List running containers
                }
            }
        }
    }

    post {
        failure {
            echo 'Deployment failed! Check logs for errors.'
        }
        success {
            echo 'Deployment successful! 🎉'
        }
    }
}
