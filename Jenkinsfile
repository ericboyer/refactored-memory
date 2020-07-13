

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
                        def withExtraChars = "${version}-" + currentBuild.number
                        devTag  = withExtraChars.replaceAll("[\r\n|\n\r|\n|\r]", "")

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
        stage('Deploy to development') {
            steps {
                container('python') {
                    sh "oc -n ${devProject} set image dc/${imageName} ${imageName}=${devProject}/${imageName}:${devTag} --source=imagestreamtag"
                    sh "oc -n ${devProject} set env dc/${imageName} VERSION=\"${devTag} (${imageName}-dev)\""
                    sh "oc -n ${devProject} rollout latest dc/${imageName}"
                    waitOnDeployment(devProject)
                }
            }
        }
        stage('Stash image in Nexus') {
            steps {
                container('skopeo') {
                    sh "echo Stash image in registry"
//                    sh "skopeo copy --src-tls-verify=false --dest-tls-verify=false --src-creds openshift:\$(oc whoami -t) --dest-creds admin:r3dh4t1 docker://${internalClusterRegistry}/${devProject}/${imageName}:${devTag} docker://${clusterRegistry}/${imageName}:${devTag}"
//                    // TBD: Tag the built image with the production tag.
//                    sh "oc -n ${prodProject} tag ${devProject}/${imageName}:${devTag} ${devProject}/${imageName}:${prodTag}"
                }
            }
        }
        stage('Execute integration tests') {
            steps {
                container('python') {
                    sh "echo Do testing"
                }
            }
        }

        stage('Promote to production') {
            steps {
                container('python') {
                    sh "echo Promote to production"
                }
            }
        }
    }
}

void waitOnDeployment(String project) {
    script {
        // Use the openshift plugin to wait for the deployment to complete
        openshift.withCluster() {
            openshift.withProject(project) {
                def dc = openshift.selector("dc", "${imageName}").object()
                def dc_version = dc.status.latestVersion
                def rc = openshift.selector("rc", "${imageName}-${dc_version}").object()
                echo "Waiting for ReplicationController ${imageName}-${dc_version} to be ready"
                while (rc.spec.replicas != rc.status.readyReplicas) {
                    sleep 5
                    rc = openshift.selector("rc", "${imageName}-${dc_version}").object()
                }
            } // withProject
        } // withCluster
    }
}