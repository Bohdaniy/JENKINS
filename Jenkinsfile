pipeline {
    options {timestamps()}
    agent none
    environment {
        DOCKER_CREDI = credentials('docker')  // Встановіть свої креденціали для Docker
        DOCKER_IMAGE_NAME = "Bohdaniy/laboratory4"  // Назва вашого Docker образу
        DOCKER_TAG = "1.11"  // Тег для вашого образу
    }
    stages {
        stage ('Check scm') {
            agent any
            steps {
                checkout scm
            }
        }
        stage ('Build') {
            agent any
            steps {
                echo "Building ... ${BUILD_NUMBER}"
                echo "Build completed"
            }
        }
        stage ('Test') {
            agent {
                docker {
                    image 'python:3.12-alpine'
                    args '-u="root"'
                }
            }
            steps {
                script {
                    // Встановлення Python і pip, створення віртуального середовища
                    sh '''
                        apk add --no-cache python3 py3-pip && \
                        python3 -m venv /venv && \
                        /venv/bin/pip install unittest-xml-reporting
                    '''
                    // Запуск тестів
                    sh '/venv/bin/python3 Testing.py'
                }
            }
            post {
                always {
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
        stage ('Build Docker Image') {
            agent any
            steps {
                script {
                    echo "Building Docker image... ${BUILD_NUMBER}"
                    // Створення Docker образу
                    sh 'docker build -t $DOCKER_IMAGE_NAME:$DOCKER_TAG .'
                }
            }
        }
        stage ('Push Docker Image to Docker Hub') {
            agent any
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    // Логін до Docker Hub за допомогою credential'ів Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'DOCKER_CREDI_PSW', usernameVariable: 'DOCKER_CREDI_USR')]) {
                        // Логін до Docker Hub
                        sh "docker login -u $DOCKER_CREDI_USR -p $DOCKER_CREDI_PSW"
                        // Завантаження Docker образу
                        sh "docker push $DOCKER_IMAGE_NAME:$DOCKER_TAG"
                    }
                }
            }
        }
    }
    post {
        always {
            echo "Cleaning up Docker images..."
            // Очистка Docker образів після завершення процесу
            script {
                sh 'docker rmi $DOCKER_IMAGE_NAME:$DOCKER_TAG'
            }
        }
    }
}
