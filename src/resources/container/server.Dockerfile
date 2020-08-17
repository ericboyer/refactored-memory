FROM registry.access.redhat.com/ubi8/python-38

ARG port
ENV port=${BIND_PORT}
ARG repo
ENV repo=${PYPI_GROUP_REPO}
ARG nexus_hostname
ENV nexus_hostname=${NEXUS_HOSTNAME}

WORKDIR /app
# Add runtime dependencies
ADD requirements.txt .

# Install package
RUN pip install -r requirements.txt && \
    pip install refactored-memory \
        --trusted-host ${nexus_hostname} \
        -i http://${nexus_hostname}/${repo}

USER 1001

EXPOSE ${port}
# BIND_PORT is optional as it's defined in the pod's env and made available via configmap; being explicit here
CMD refactored-memory-server --port=${port}