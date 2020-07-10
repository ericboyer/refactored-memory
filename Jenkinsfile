

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
                    sh 'python3 -m pip install --upgrade setuptools wheel twine'
                    sh 'python3 -m pip install --upgrade -r requirements.txt'
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
            // Build Image (binary build), tag Image
            // Make sure the image name is correct in the tag!
            sh "oc -n ${devProject} start-build bc/${imageName}"
            sh "oc -n ${devProject} tag ${devProject}/${imageName}:latest ${devProject}/${imageName}:${devTag}"

//                # Set up Dev Application (binary build strategy)
//                oc new-build --binary=true --name=${app} openjdk-11-rhel8:latest -n ${project}
//                oc set build-secret --pull bc/${app} redhatio
//                oc new-app ${project}/${app}:0.0-0 --name=${app} --allow-missing-imagestream-tags=true -n ${project}
//                oc set triggers dc/${app} --remove-all -n ${project}
//                oc expose dc ${app} --port 8080 -n ${project}
//                oc expose svc ${app} -n ${project}
//                oc set probe dc/${app} -n ${project} --readiness --failure-threshold 3 --initial-delay-seconds 5 --get-url=http://:8080/actuator/health
//
//                # setup first application tagged as latest
//                pushd hello-spring
//                ./gradlew clean bootjar
//                oc start-build bc/helloworld --from-file=./build/libs/helloworld-0.0.1.jar
        }
        stage('Deploy') {
            steps {

            }
        }
    }
}