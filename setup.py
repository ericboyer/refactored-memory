from setuptools import setup
import os

with open("README.md", "r") as fh:
    long_description = fh.read()
# review https://amir.rachum.com/blog/2017/07/28/python-entry-points/ for improvements
setup(
    name='refactored-memory',
    version='0.0.{}'.format(os.environ["BUILD_NUMBER"]),
    author="Black Label",
    author_email="eboyer@redhat.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericboyer/refactored-memory.git",
    packages=["net"],
    # packages=setuptools.find_packages(),
    # include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'refactored-memory-server = net.server:main',
            'refactored-memory-client = net.client:main',
        ],
    }
)