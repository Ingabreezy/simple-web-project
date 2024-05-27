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
                    bat 'docker-compose -f docker-compose.template.yml build'
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

                    // Replace the placeholder in the docker-compose file with the actual port
                    bat """
                    type docker-compose.template.yml | `
                    powershell -Command "foreach ($line in Get-Content -Path 'docker-compose.template.yml') { `
                        $line -replace '\\${DYNAMIC_PORT}', '${env.DYNAMIC_PORT}' `
                    }" > docker-compose.yml
                    """
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
