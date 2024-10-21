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
                    image 'alpine'
                    args '-u="root"'
                }
            }
            steps {
                script {
                    // Установка необхідних залежностей
                    sh 'apk add --update py3-pip py3-setuptools py3-wheel'
                    sh 'pip install xmlrunner'
                    sh 'python3 -m venv /venv'
                    sh '. /venv/bin/activate && pip install unittest-xml-reporting'
                }

                // Запуск тестів
                sh 'python3 Testing.py'
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
