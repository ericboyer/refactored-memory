FROM registry.access.redhat.com/ubi8/python-38

ARG port=${BIND_PORT}
ARG repo=${PYPI_GROUP_REPO}

EXPOSE ${port}

RUN pip install refactored-memory -i ${repo} && echo "port=${port} repo=${repo}"

# BIND_PORT is optional as it's defined in the pod's env and made available via configmap
CMD python3 refactored-memory-server --port=${port}