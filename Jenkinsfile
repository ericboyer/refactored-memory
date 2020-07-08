//environment {
//    imageName = "refactored-memory"
//    devProject = "${imageName}-dev"
//    prodProject = "${imageName}-prod"
//    devTag = "0.0-0"
//    prodTag = ""
//    destApp     = "${imageName}-green"
//    activeApp   = ""
//}

pipeline {
    agent {
        kubernetes {
            label "python-38"
            cloud "openshift"
            serviceAccount "jenkins"
            containerTemplate {
                name "python"
                image "docker-registry.default.svc:5000/ebo-cicd/python-38:latest"
                resourceRequestMemory "1Gi"
                resourceLimitMemory "1Gi"
                resourceRequestCpu "1"
                resourceLimitCpu "1"
            }
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m pip install --user --upgrade setuptools wheel'
                sh 'python3 setup.py sdist bdist_wheel'
            }
        }
        stage('Test') {
            steps {
                sh 'echo Placeholder for unit tests'
            }
        }
        stage('Publish') {
            steps {
                sh 'python3 -m pip install --user --upgrade twine'
                sh 'python3 -m twine upload -r pypi-internal dist/*'
            }
        }
    }
}