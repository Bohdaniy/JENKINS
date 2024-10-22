pipeline {
    options {timestamps()}
    agent none
    environment {
        DOCKER_CREDI = credentials('docker')
    }
    stages {
        stage ('Check scm') {
            agent any
            steps {
                checkout scm
            }
        }
        stage ('Build') {
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
        }
    stage ('Publishing to Docker') {
        agent any
        steps {
            sh 'echo $DOCKER_CREDI_PSW | docker login --username $DOCKER_CREDI_USR --password-stdin'
            sh 'docker build -t bohdaniy/laboratory4 --push .'

        }
        post {
            always {
                sh 'docker logout'
            }
        }
    }
    }
}
    }
}