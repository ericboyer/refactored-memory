from setuptools import setup, find_namespace_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='refactored-memory',
    version='1.0.0',
    author="eboyer",
    author_email="eboyer@redhat.com",
    description="Python client/server application to demonstrate pipelines on OpenShift.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # install_requires=["docopt~=0.6.2", "Flask~=1.1.2"],
    url="https://github.com/ericboyer/refactored-memory.git",
    package_dir={"": "src"},
    # packages=find_namespace_packages(include="refactored-memory.*"),
    packages=find_namespace_packages(where="src"),
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'refactored-memory-server = refactored_memory.net.server:main',
            'refactored-memory-client = refactored_memory.net.client:main',
            'refactored-memory-rest-client = refactored_memory.web.app:main'
        ],
    }
)
