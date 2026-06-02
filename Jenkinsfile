pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Lint') {
            steps {
                echo 'Checking Python syntax...'
                sh 'python -m py_compile app/calculator.py'
                echo 'Syntax check passed.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    python -m pytest tests/ \
                        -v \
                        --tb=short \
                        --junitxml=test-results.xml \
                        --cov=app \
                        --cov-report=term-missing
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build') {
            steps {
                echo "Build number: ${env.BUILD_NUMBER}"
                echo "Job name: ${env.JOB_NAME}"
                echo 'Packaging would happen here in a real project.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed — check stage logs above.'
        }
    }
}
