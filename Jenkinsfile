pipeline {
    agent any

    environment {
        // Use Jenkins Credentials Plugin to manage sensitive information
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gdrive-service-account')
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Set the path for the Google credentials
                    env.GOOGLE_APPLICATION_CREDENTIALS_PATH = "${env.WORKSPACE}/service-account-credentials.json"
                    writeFile file: env.GOOGLE_APPLICATION_CREDENTIALS_PATH, text: GOOGLE_APPLICATION_CREDENTIALS
                }
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python scrapper.py'
            }
        }

        stage('Upload to Google Drive') {
            steps {
                withEnv(["GOOGLE_APPLICATION_CREDENTIALS=${env.GOOGLE_APPLICATION_CREDENTIALS_PATH}"]) {
                    sh 'python upload_to_drive.py'
                }
            }
        }
    }

    post {
        always {
            // Clean up sensitive files
            sh 'rm -f ${env.GOOGLE_APPLICATION_CREDENTIALS_PATH}'
        }
    }
}
