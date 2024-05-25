pipeline {
    agent any

    environment {
        DYNAMIC_PORT = "8082"
        CONTAINER_NAME = "simple-web-container-${env.BUILD_ID}"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo "Starting Build: ${new Date()}"
                    bat 'docker-compose build'
                    echo "Build Completed: ${new Date()}"
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo "Starting Test: ${new Date()}"
                    // Ensure any existing container is stopped and removed
                    bat 'docker-compose down'
                    // Start the container
                    bat 'docker-compose up -d'
                    // Adding a delay to ensure the server is up before running tests
                    bat '''
                    @echo off
                    ping 127.0.0.1 -n 6 > nul
                    '''
                    bat 'docker-compose exec web python test_script.py'
                    bat 'docker-compose down'
                    echo "Test Completed: ${new Date()}"
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo "Starting Deploy: ${new Date()}"
                    // Ensure any existing container is stopped and removed
                    bat 'docker-compose down'
                    // Start the container
                    bat 'docker-compose up -d'
                    echo "Deploy Completed: ${new Date()}"
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
