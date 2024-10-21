pipeline {
    options {timestamps()}
    agent none
    environment{
        DOCKER_CREDI = credentials('docker')
    }
    stages{
        stage ('Check scm'){
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
            agent { docker { image 'alpine' 
                            args '-u=\"root\"'}
                    }
            steps {
                sh 'apk add --update python3 py-pip'
                sh 'python3 -m venv /venv'
                sh 'source /venv/bin/activate && pip install unittest-xml-reporting'
                sh 'source /venv/bin/activate && python3 Testing.py'
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