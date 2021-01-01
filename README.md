# Versioning CLI
### Semantic Versioning CLI tool

### About

A command line program to generate semantic versioning for Git. 
Can be used mainly in CI/CD pipelines.

### Usage example

```shell
versioning init --initial-version=1.0.0.BUILD-SNAPSHOT
```

The command about will initialise versioning for a new repository.
Execute the next command to push the changes:


```shell
versioning push
```

In consequence the program will tag `1.0.0.BUILD-SNAPSHOT` in current 
git head branch and push to remote.

## Details

This program supports four cycles of versioning for the same semantic version:
- BUILD-SNAPSHOT
- MILESTONE 1, 2, 3, ...
- RELEASE_CANDIDATE 1, 2, 3, ...
- RELEASE



## Technical Details

### CLI Options

```shell
--initial-version
```
Used to initialise a project without any semantic version in git. 
This option requires the full `output semantic version formmat`. 

```shell
--tag RELEASE_CANDIDATE
```

