Notes on OpenShift setup required to support this app (assuming jenkins and supporting 
ci/cd infrastructure is deployed)

Create project:

```
oc new-project refactored-memory-dev
oc new-project refactored-memory-prod
```

Create pipeline buildconfig:
```
oc policy add-role-to-user edit system:serviceaccount:ebo-cicd:jenkins -n ${project-dev}
oc policy add-role-to-user edit system:serviceaccount:ebo-cicd:jenkins -n ${project-prod}
```

Give jenkins access to the projects:

Create configmap for build:

```oc create configmap refactored-memory --from-file=/Users/eboyer/.pypirc --from-literal=BIND_PORT=8088 --from-literal=PYPI_GROUP_REPO=http://nexus-ebo-cicd.apps.ccsd3.rht-labs.com/repository/pypi-public/simple```

Create app deployment config:

```oc new-app refactored-memory-dev/refactored-memory:0.0-0 --allow-missing-imagestream-tags=true -n refactored-memory-dev```
