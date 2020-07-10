Import image into working namespace (refactored-memory):

```oc import-image ubi8/python-38 --from=registry.access.redhat.com/ubi8/python-38 --confirm```

List imported image:

```
MacBook-Pro:refactored-memory eboyer$ oc get is
   NAME        DOCKER REPO                                                    TAGS     UPDATED
   python-38   docker-registry.default.svc:5000/refactored-memory/python-38   latest   About a minute ago
```