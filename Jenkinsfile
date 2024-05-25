pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building the Docker image...'
                    bat 'docker build -t simple-web-project .'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    // Stop and remove any existing container with the same name
                    bat '''
                    docker stop simple-web-container || true
                    docker rm simple-web-container || true
                    docker run --rm -d -p 8082:8080 --name simple-web-container simple-web-project
                    '''
                    // Adding a delay to ensure the server is up before running tests
                    bat '''
                    @echo off
                    ping 127.0.0.1 -n 6 > nul
                    '''
                    bat 'docker exec simple-web-container python test_script.py'
                    bat 'docker stop simple-web-container'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the Docker container...'
                    // Stop and remove any existing container with the same name before deployment
                    bat '''
                    docker stop simple-web-container || true
                    docker rm simple-web-container || true
                    docker run -d -p 8082:8080 --name simple-web-container simple-web-project
                    '''
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
