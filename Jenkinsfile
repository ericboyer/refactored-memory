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
            cloud "openshift"
            label "build-pod"
            serviceAccount "jenkins"
            yamlFile "openshift/templates/build-pod.yaml"
        }
    }
    stages {
//        node('python')
        stage('Build') {
            container('python') {
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