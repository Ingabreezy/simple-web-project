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
                    bat 'docker run --rm -d -p 8000:8000 --name simple-web-container simple-web-project'
                    // Adding a delay to ensure the server is up before running tests
                    bat 'timeout /T 5'
                    bat 'docker exec simple-web-container python test_script.py'
                    bat 'docker stop simple-web-container'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the Docker container...'
                    bat 'docker run -d -p 8000:8000 simple-web-project'
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
