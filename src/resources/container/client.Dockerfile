FROM registry.access.redhat.com/ubi8/python-38

ARG port
ENV port=${BIND_PORT}
ARG repo
ENV repo=${PYPI_GROUP_REPO}
ARG nexus_hostname
ENV nexus_hostname=${NEXUS_HOSTNAME}
ARG namespace
ENV namespace=${NAMESPACE}

WORKDIR /app
# Add runtime dependencies
ADD requirements.txt .

# Install app and dependencies
RUN pip install -r requirements.txt && \
    pip install refactored-memory \
        --trusted-host ${nexus_hostname} \
        -i http://${nexus_hostname}/${repo}

USER 1001

EXPOSE 5000
ENV SERVER_PORT=${port}
ENV SERVER_IP=${refactored-memory-server.${namespace}.svc.cluster.local}
# BIND_PORT is optional as it's defined in the pod's env and made available via configmap; being explicit here
CMD refactored-memory-rest-client
#ENTRYPOINT FLASK_APP=refactored_memory/web/app.py flask run --host=0.0.0.0