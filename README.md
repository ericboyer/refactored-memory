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
```TBD```

# Run server
```python3 ```