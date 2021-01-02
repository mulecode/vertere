# Versioning CLI
### Semantic Versioning CLI tool

### About

A command line program to generate semantic versioning for Git. 

### Basic usage - Initialise versioning
Scenario - Given a project with Git initialised and with no semantic version tags.

```shell
▶ versioning init init --initial-version=v1.0.0
Initialising project with version: v1.0.0

```

The command above will prepare the project for a git tag `v1.0.0`
but it won't commit either push to git. 

Execute the next command to commit and push the changes to remote:

```shell
▶ versioning push
Tag v1.0.0 pushed.
```

The push command will tag `v1.0.0` in current 
git head branch and push to remote.


### Basic usage - Versioning Patch, Minor or Major
Scenario - Given a project with Git initialised and already initialised with a 
semantic version git tag.

```shell
▶ versioning init --incrementer=patch --prefix v
Found highest tag: v1.0.0
Next version v1.0.1
```
Then execute `versioning push` command to push to git.

### Supported postfix

- BUILD-SNAPSHOT
- M[sequencer]
- RC[sequencer]
- RELEASE

**Details**

BUILD-SNAPSHOT - This postfix is configured to be not promotable, 
this means that if the `highest tag` is equals to `1.0.0.BUILD-SNAPSHOT` the 
next tag will be the same, and the push command will delete the previous tag and 
commit it again in the HEAD of the current branch.
