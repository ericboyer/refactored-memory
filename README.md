# refactored-memory
Simple TCP server in python

# Prereqs
* Gradle 6+
* Python 3.7+

# Build w/gradle
```gradle clean build``` or ```./gradlew clean build```

# Push to nexus
```python3 -m twine upload --repository-url <repo_url> build/distributions/*```

> repo_url = http://nexus-ebo-cicd.apps.ccsd3.rht-labs.com/repository/pypi-public/

# Install package
```
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload -r pypi-internal dist/*
```

# Run server
```pip3.8 install tcpserver```

