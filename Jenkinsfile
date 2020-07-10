

pipeline {
    environment {
        imageName = "refactored-memory"
        devProject = "${imageName}-dev"
        prodProject = "${imageName}-prod"
        devTag = "0.0-0"
        prodTag = ""
        destApp     = "${imageName}-green"
        activeApp   = ""
    }
    agent {
        kubernetes {
            cloud "openshift"
            label "build-pod"
            serviceAccount "jenkins"
            yamlFile "openshift/build-pod.yaml"
        }
    }
    stages {
        stage('Setup Python prereqs') {
            steps {
                container('python') {
                    sh 'python3 --version'
                    sh 'python3 -m pip install --user --upgrade setuptools wheel twine'
                    sh 'python3 -m pip install --user --upgrade -r requirements.txt'
                }
            }
        }
        stage('Build source and build distribution') {
            steps {
                container('python') {
                    sh 'python3 setup.py sdist bdist_wheel'
                }
            }
        }
        stage('Test stuff') {
            steps {
                sh 'echo Placeholder for unit tests'
            }
        }
        stage('Publish to Nexus') {
            steps {
                container('python') {
                    sh 'python3 -m twine upload --config-file /etc/config/.pypirc -r pypi-internal dist/*'
                }
            }
        }
        stage('Build and Tag OpenShift Image') {
            steps {
                container('python') {
                    // Build Image (binary build), tag Image
                    // Make sure the image name is correct in the tag!
                    sh "oc -n ${devProject} start-build bc/${imageName}"
                    // wait, hack for now
                    sh "sleep 60"
                    sh "oc -n ${devProject} tag ${devProject}/${imageName}:latest ${devProject}/${imageName}:${devTag}"
                }
            }
        }
        stage('Deploy') {
            steps {
                sh "echo Placeholder for deployment instructions"
            }
        }
    }
}