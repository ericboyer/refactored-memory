Notes on OpenShift setup required to support this app:

Create project:

```oc new-project refactored-memory-dev```

Create configmap for build:

```oc create configmap refactored-memory --from-file=/Users/eboyer/.pypirc --from-literal=BIND_PORT=8088 --from-literal=PYPI_GROUP_REPO=http://nexus-ebo-cicd.apps.ccsd3.rht-labs.com/repository/pypi-public/simple```

