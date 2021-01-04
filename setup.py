from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vertere',
    packages=find_packages(include=['vertere']),
    version='1.0.0',
    description='Vertere is a simple semantic versioning cli program that uses git tags to versioning',
    long_description=long_description,
    author='Rafael Mule',
    author_email='rafael@mulecode.co.uk',
    url='github.com',
    license='MIT',
    install_requires=[
        'click==7.1.2',
        'GitPython==3.1.11',
        'PyYAML==5.3.1'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest==6.2.1',
        'pytest-mock==3.4.0'
    ],
    test_suite='tests',
    include_package_data=True,
    package_data={'vertere': ['data/*.json']},
    entry_points={
        'console_scripts': [
            'vertere = vertere.vertere:cli'
        ]
    }
)
