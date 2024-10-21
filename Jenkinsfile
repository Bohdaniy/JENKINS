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
                    script {
    // Установка необхідних залежностей
                 sh 'apk add --update python3 py-pip'
                 sh 'python3 -m venv /venv'

    // Активуємо віртуальне середовище і встановлюємо пакети
                 sh '. /venv/bin/activate && pip install unittest-xml-reporting xmlrunner'

    // Запускаємо тести
    sh '. /venv/bin/activate && python3 Testing.py'
}

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
