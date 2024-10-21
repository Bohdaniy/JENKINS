pipeline {
    options { timestamps() }
    agent none
    environment {
        DOCKER_CREDI = credentials('docker_hub')
    }
    stages {
        stage('Check scm') {
            agent any
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo "Building ... ${BUILD_NUMBER}"
                echo "Build completed"
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'alpine'
                    args '-u="root"'
                }
            }
            steps {
                // Установка необхідних залежностей
                sh 'apk add --update python3 py-pip'
                sh 'python3 -m venv /venv'
                sh 'pip install unittest-xml-reporting'

                // Запуск тестів
                sh 'python3 Lab5/Test.py'
            }
            post {
                always {
                    // Публікація результатів тестів у форматі JUnit
                    junit 'test-reports/*.xml'
                }
                success {
                    echo "Testing successful"
                }
                failure {
                    echo "Tests failed"
                }
            }
        }
    }
}
