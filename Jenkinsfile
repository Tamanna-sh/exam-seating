pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat 'venv\\Scripts\\python -m pytest'
            }
        }
        stage('Docker Build') {
            steps {
                bat 'docker build -t exam-seating .'
            }
        }
        stage('Deploy') {
            steps {
                bat 'docker rm -f exam-seating-app || exit /b 0'
                bat 'docker run -d --name exam-seating-app -p 5000:5000 exam-seating'
            }
        }
    }
}