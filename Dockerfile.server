FROM registry.access.redhat.com/ubi8/python-38

ARG port
ENV port = ${BIND_PORT}
ARG repo
ENV repo = ${PYPI_GROUP_REPO}

EXPOSE ${port}

RUN pip install refactored-memory -i ${repo}

# BIND_PORT is optional as it's defined in the pod's env and made available via configmap
CMD["python3", "refactored-memory-server", "--port=${port}"]