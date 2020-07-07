# refactored-memory
Simple python TCP client/server that sends and prints text that user enters via console.

# Prereqs
* Gradle 6+ (TODO)
* Python 3.8+
* .pypirc configured for cluster access to `pypi-public` repository
* SERVER_PORT env var set in server runtime


# Build source and built distribution
```
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload -r pypi-internal dist/*
```

# Push to nexus
```python3 -m twine upload --repository-url <repo_url> dist/*```

> repo_url = http://nexus-ebo-cicd.apps.ccsd3.rht-labs.com/repository/pypi-public/

or with .pypirc config:

```python3 -m twine upload -r pypi-internal dist/*```
# Install package
```
pip3.8 install refactored-memory
```

# Run server
```python3 net/server.py```

> SERVER_PORT must be set in env

