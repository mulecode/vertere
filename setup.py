from setuptools import find_packages, setup

setup(
    name='versioning',
    packages=find_packages(include=['versioning']),
    version='1.0.0',
    description='My first Python library',
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
    package_data={'versioning': ['data/*.json']},
    # package_data={'': ['*.json']},
    entry_points={
        'console_scripts': [
            'versioning = versioning.versioning:cli'
        ]
    }
)
