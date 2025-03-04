pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/yuvrajpradhan/Fitness_track_301P'
            }
        }

        stage('Build and Start Containers') {
            steps {
                script {
                    bat 'docker-compose down'
                    bat 'docker-compose pull' // Pull latest images (if any)
                    bat 'docker-compose build --no-cache' // Ensure fresh build
                    bat 'docker-compose up -d' // Start containers
                }
            }
        }

        stage('Post Deployment Check') {
            steps {
                script {
                    bat 'docker ps' // Verify running containers
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Deployment successful! 🎉'
        }
        failure {
            echo 'Deployment failed! Check logs for errors.'
        }
    }
}
