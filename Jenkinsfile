stage('Test') {
    agent {
        docker {
            image 'python:3.12-alpine'
            args '-u="root"'
        }
    }
    steps {
        script {
            try {
                // Установка необхідних залежностей
                echo "Installing dependencies..."
                sh 'apk add --update python3 py-pip gcc musl-dev'
                sh 'python3 -m venv /venv'

                // Активуємо віртуальне середовище і встановлюємо пакети
                echo "Activating virtual environment and installing packages..."
                sh '. /venv/bin/activate && pip install unittest-xml-reporting xmlrunner'

                // Запускаємо тести
                echo "Running tests..."
                sh '. /venv/bin/activate && python3 Testing.py'
            } catch (e) {
                echo "Error during the test stage: ${e}"
                throw e
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
