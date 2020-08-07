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

- Deploy Jenkins and update plugins (manually)

    `oc new-app --template jenkins-persistent -p VOLUME_CAPACITY=2G`
    
- Deploy SonarQube
    ```
    oc new-app --docker-image=sonarqube
    oc expose svc/sonarqube
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

Give jenkins access to the dev and prod projects:
```
oc policy add-role-to-user edit system:serviceaccount:ebo-cicd:jenkins -n ${project-dev}
oc policy add-role-to-user edit system:serviceaccount:ebo-cicd:jenkins -n ${project-prod}
```

Create configmap for build:

```oc create configmap refactored-memory --from-file=/Users/eboyer/.pypirc --from-literal=BIND_PORT=8088 --from-literal=PYPI_GROUP_REPO=http://nexus-ebo-cicd.apps.ccsd3.rht-labs.com/repository/pypi-public/simple```

Create app deployment config:

```oc new-app refactored-memory-dev/refactored-memory:0.0-0 --allow-missing-imagestream-tags=true -n refactored-memory-dev```

Disable automatic deployments (for example, ImageStream change event)

Add readiness and liveness health checks, if applicable.