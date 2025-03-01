pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Pull code from Git repository
                echo 'checkout'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'install dependencies'
        }

        stage('Run Tests') {
            steps {
               echo 'running tests'
            }
        }

        stage('Build') {
            steps {
                echo 'Build'
            }
        }

        stage('Deploy') {
            steps {
                // Deploy to your server (e.g., using Docker, Ansible, or SSH)
                echo 'deploy' // Example for Docker
            }
        }
    }
    }
}