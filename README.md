# refactored-memory
Simple python client/server that sends and prints text that user enters via console. The server is intended to run
as a container in OpenShift. To connect via client app, run `oc port-forward <pod> <local-port>:<pod-port>` then 
invoke client with something like: `refactored-memory-client --server_ip=127.0.0.1 --server_port=<local-port>`.
