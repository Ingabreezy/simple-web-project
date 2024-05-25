pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    echo "Starting Build: ${new Date()}"
                    bat 'docker build -t simple-web-project .'
                    echo "Build Completed: ${new Date()}"
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo "Starting Test: ${new Date()}"
                    // Ensure any existing container is stopped and removed
                    bat '''
                    docker stop simple-web-container || exit 0
                    docker rm simple-web-container || exit 0
                    '''
                    bat '''
                    docker run --rm -d -p 8082:8080 --name simple-web-container simple-web-project
                    '''
                    // Adding a delay to ensure the server is up before running tests
                    bat '''
                    @echo off
                    ping 127.0.0.1 -n 6 > nul
                    '''
                    bat 'docker exec simple-web-container python test_script.py'
                    bat 'docker stop simple-web-container'
                    echo "Test Completed: ${new Date()}"
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo "Starting Deploy: ${new Date()}"
                    // Ensure any existing container is stopped and removed
                    bat '''
                    docker stop simple-web-container || exit 0
                    docker rm simple-web-container || exit 0
                    '''
                    bat '''
                    docker run -d -p 8082:8080 --name simple-web-container simple-web-project
                    '''
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
