pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fitness-tracker'
        DOCKER_TAG = 'latest'
        POSTGRES_USER = 'admin'
        POSTGRES_PASSWORD = credentials('postgres-password') // Use Jenkins credentials
        POSTGRES_DB = 'fitness_db'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yuvrajpradhan/Fitness_track_301P'
            }
        }

        stage('Build React App') {
            steps {
                sh '''
                  cd client
                  npm install || exit 1
                  npm run build || exit 1
                '''
            }
        }

        stage('Set Up Django') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python manage.py migrate'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Run Docker Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python manage.py test'
                sh 'cd frontend && npm test'
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}