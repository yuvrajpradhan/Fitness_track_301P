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
                    sh 'docker-compose pull' // Pull latest images (if any)
                    sh 'docker-compose build --no-cache' // Ensure fresh build
                    sh 'docker-compose up -d' // Start containers
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'docker exec backend_container_name python manage.py test' // Replace with actual container name
                }
            }
        }

        stage('Post Deployment Check') {
            steps {
                script {
                    sh 'docker ps' // Verify running containers
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
