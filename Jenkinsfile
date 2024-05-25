pipeline {
    agent any

    environment {
        CONTAINER_NAME = "simple-web-container-${env.BUILD_ID}"
    }

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
        stage('Find Free Port') {
            steps {
                script {
                    def port = bat(script: 'python find_free_port.py', returnStdout: true).trim()
                    env.DYNAMIC_PORT = port
                    echo "Selected free port: ${env.DYNAMIC_PORT}"
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo "Starting Test: ${new Date()}"
                    // Ensure any existing container with the same name is stopped and removed
                    bat '''
                    docker stop ${CONTAINER_NAME} || exit 0
                    docker rm ${CONTAINER_NAME} || exit 0
                    '''
                    // Run the container with the dynamically chosen port
                    bat "docker run --rm -d -p ${env.DYNAMIC_PORT}:8080 --name ${CONTAINER_NAME} simple-web-project"
                    // Adding a delay to ensure the server is up before running tests
                    bat '''
                    @echo off
                    ping 127.0.0.1 -n 6 > nul
                    '''
                    bat "docker exec ${CONTAINER_NAME} python test_script.py"
                    bat "docker stop ${CONTAINER_NAME}"
                    echo "Test Completed: ${new Date()}"
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo "Starting Deploy: ${new Date()}"
                    // Ensure any existing container with the same name is stopped and removed
                    bat '''
                    docker stop ${CONTAINER_NAME} || exit 0
                    docker rm ${CONTAINER_NAME} || exit 0
                    '''
                    // Run the container with the dynamically chosen port
                    bat "docker run -d -p ${env.DYNAMIC_PORT}:8080 --name ${CONTAINER_NAME} simple-web-project"
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
