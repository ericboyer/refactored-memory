Notes on OpenShift setup required to support this app (assuming jenkins and supporting 
ci/cd infrastructure is deployed)

## Initialize CI/CD:
> namespace:  ebo-cicd

- Deploy GitLab (runners will be deployed later)
    ```
    oc new-app --name gitlab --docker-image gitlab/gitlab-ce:latest
    # TODO - add readiness and liveness (takes like 3 minutes to initialize)
    oc create sa gitlab-sa
    oc set serviceaccount deploymentconfig gitlab gitlab-sa
    oc expose svc/gitlab --port 80
    oc adm policy add-scc-to-user anyuid -z gitlab-sa
    oc policy add-role-to-user cluster-admin -z gitlab-sa
    ```

- Deploy `Nexus Repository Operator` in cicd namespace and run the following:
    ```
    oc set serviceaccount deployment nexusrepo-sonatype-nexus nxrm-operator-certified
    oc policy add-role-to-user cluster-admin -z nxrm-operator-certified
    oc expose svc/nexusrepo-sonatype-nexus-service
    ```
  > Node: Don't forget to configure pypi (hosted -> pypi-dev, group -> pypi-public (w/pypi-dev))

- Deploy Jenkins and update plugins (manually)

    `oc new-app --template jenkins-persistent -p VOLUME_CAPACITY=2G`
    
- Deploy SonarQube
    ```
    oc new-app --docker-image=sonarqube
    oc expose svc/sonarqube
    ```
  
- Deploy custom `python-builder`
    ```
    oc new-project ebo-python-builder
    oc create secret generic githubssh --from-file=ssh-privatekey=/Users/eboyer/github
    oc process -f https://raw.githubusercontent.com/rht-ccsd/sitr/feature/python-runtime/openshift/python-builder/python-builder.yaml \
        | oc create -f -
    oc policy add-role-to-group  \
        -n ${RHT_OCP4_DEV_USER}-common system:image-puller \
        system:serviceaccounts:${RHT_OCP4_DEV_USER}-expose-image
    ```

## Setup application
- Create project:

    ```
    oc new-project refactored-memory-dev
    oc new-project refactored-memory-prod
    ```

- Create pipeline buildconfig:

    `oc -n ebo-cicd new-build --name refactored-memory-pipeline --strategy pipeline https://github.com/ericboyer/refactored-memory.git#master`

> Add secrets if repo is private

Create configmap for build:

    ```
    oc create configmap pipeline-config --from-file=/Users/eboyer/.pypirc \
        --from-literal=BIND_PORT=8088 \
        --from-literal=PYPI_GROUP_REPO=http://nexus-ebo-cicd.apps.ccsd3.rht-labs.com/repository/pypi-public/simple
    ```
or

`oc -n ebo-cicd create cm pipeline-config -f src/resources/openshift/cm.yaml`

Give jenkins access to the dev and prod projects:
```
oc policy add-role-to-user edit system:serviceaccount:ebo-cicd:jenkins -n ${project-dev}
oc policy add-role-to-user edit system:serviceaccount:ebo-cicd:jenkins -n ${project-prod}
```


Create app deployment config, imagestream, svc, and route (client only):

```oc new-app refactored-memory-dev/refactored-memory:0.0-0 --allow-missing-imagestream-tags=true -n refactored-memory-dev```

Disable automatic deployments (for example, ImageStream change event)

Add readiness and liveness health checks, if applicable.

- Enable/configure github webhooks