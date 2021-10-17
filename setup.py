
from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='backoid',
    description='backoid',
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'pymysql>=0.9.3',
        'azure-storage-blob',
        'pyyaml'
    ],
    classifiers=[
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'console_scripts': [
           'backoid = backoid.cli:main'
        ]
    }
)
