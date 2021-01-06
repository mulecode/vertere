from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vertere',
    packages=find_packages(include=['vertere', 'data']),
    version='1.0.0.dev1',
    description='Vertere is a simple semantic versioning cli program that uses git tags for persisting',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rafael Mule',
    author_email='rafael@mulecode.co.uk',
    url='https://github.com/mulecode/vertere',
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
    package_data={'': ['data/*.json']},
    entry_points={
        'console_scripts': [
            'vertere = vertere.vertere:cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
