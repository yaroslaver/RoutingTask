pipeline {
    agent {
        docker {
            image 'yaroslaver/routing-task-test'
            args '--shm-size=1g -u root'
        }
    }

    stages {
        stage('test') {
            steps {
                sh "pytest src/"
            }
        }
    }
}