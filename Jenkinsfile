

pipeline {
    environment {
        imageName = "refactored-memory"
        devProject = "${imageName}-dev"
        prodProject = "${imageName}-prod"
        // TODO Fix devTag to start with the most recent successful build
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
        stage('Collect version info') {
            steps {
                container('python') {
                    script {
                        def version = sh(returnStdout: true, script: "python3 setup.py --version | cut -f1,2 -d.")
                        // Set the tag for the development image: version + build number
                        devTag  = "${version}-${BUILD_NUMBER}"
                        // Set the tag for the production image: version
                        prodTag = "${version}"

                        echo "devTag: ${devTag}"
                        echo "prodTag: ${prodTag}"
                    }
                }
            }
        }
        stage('Setup Python prereqs') {
            steps {
                container('python') {
                    sh 'python3 --version'
                    sh 'python3 -m pip install --user --upgrade setuptools wheel twine'
                    sh 'python3 -m pip install --user --upgrade -r requirements.txt'
                }
            }
        }
        stage('Build source and build distribution artifacts') {
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
        stage('Build and tag OpenShift image') {
            steps {
                container('python') {
                    // Build Image (binary build), tag Image
                    // Make sure the image name is correct in the tag!
                    sh "oc -n ${devProject} start-build bc/${imageName} --wait"
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