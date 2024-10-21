pipeline {
    options { timestamps() }
    agent none
    environment {
        DOCKER_CREDI = credentials('docker')
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
                    image 'python:3.12-alpine'
                    args '-u="root"'
                }
            }
            steps {
                script {
                    // Установка необхідних залежностей
                    sh 'pip install --upgrade pip'
                    sh 'pip install xmlrunner unittest-xml-reporting'

                    // Створення та активація віртуального середовища
                    sh 'python3 -m venv /venv'
                    sh '. /venv/bin/activate'

                    // Запуск тестів
                    sh 'python3 Testing.py'
                }
            }
            post {
                always {
                    // Публікація результатів тестів у форматі JUnit
                    junit 'test-reports/test_results.xml'
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
