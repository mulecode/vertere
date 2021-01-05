# Vertere
### Semantic Versioning CLI tool

### About

A command line program to generate semantic versioning for Git. 

### Basic usage - Initialise versioning
Scenario - Given a project with Git initialised and with no semantic version tags.

```shell
> vertere init --initial-version=v1.0.0
Initialising project with version: v1.0.0
```

The command above will prepare the project for a git tag `v1.0.0`
but it won't commit either push to git. 

Execute the next command to commit and push the changes to remote:

```shell
> vertere push
Tag v1.0.0 pushed.
```

The push command will tag `v1.0.0` in current 
git head branch and push to remote.


### Basic usage - Versioning Patch, Minor or Major
Scenario - Given a project with Git initialised and already initialised with a 
semantic version git tag.

```shell
> vertere init --incrementer=patch --prefix v
Found highest tag: v1.0.0
Next version v1.0.1
```
Then execute `vertere push` command to push to git.

### Supported prefix

Vertere supports prefixes that can change how to print the version.

```shell
> vertere init --prefix v
```

**Important!** Prefixes should contain string values only and no blank spaces.

### Supported postfix

- BUILD-SNAPSHOT
- M[sequencer]
- RC[sequencer]
- RELEASE

Version with postfix structure:
```
1.2.3.<Postfix><Sequencer>
```

**Details**

BUILD-SNAPSHOT - This postfix is configured to be not promotable, 
this means that if the `highest tag` is equals to `1.0.0.BUILD-SNAPSHOT` the 
next tag will be the same, and the push command will delete the previous tag and 
commit it again in the HEAD of the current branch.
 
Milestone and Release-Candidate (M and RC) - Those are postfixes with auto sequencers,
if the latest tag have same postfix (M or RC). The `vertere init` command will
incrementer the sequencer only. Example from a tag `1.2.3RC4` -> `1.2.3RC5`

RELEASE - This postfix means a end version. Any promotion from a previous 
version postfix with Release will increment the semantic version. Example from
`1.2.3.RELEASE` and properties set to `--incrementer=MINOR --postfix=RELEASE` will generate
a version: `1.3.0.RELEASE`

### Postfix weights Details

All tags have a weight value that is used in the version promotion, where this 
program will use to determine what to promote.

**Important!** A version without postfix have the highest weight of all configured
postfixes.

Version ordering example: highest to lowest

```
1.1.0.BUILD-SNAPSHOT
1.0.0
1.0.0.RELEASE
1.0.0.RC1
1.0.0.M2
1.0.0.M1
1.0.0.BUILD-SNAPSHOT 
```

**Important!** prefixes do not interfere in version ordering

### Promotion Scenarios - examples

**Scenario 1:**

From: `v1.2.3`

Config: `vertere init --prefix=vv --incrementer=PATCH`

Result: `vv1.2.4`


**Scenario 2:**

From: `v1.2.3`

Config: `vertere init --prefix=v --incrementer=PATCH --postfix=RC`

Result: `v1.2.4.RC1`

**Scenario 3:**

From: `v1.2.4.RC1`

Config: `vertere init --prefix=v --incrementer=PATCH --postfix=RC`

Result: `v1.2.4.RC2`

**Scenario 4:**

From: `v1.2.4.RC2`

Config: `vertere init --prefix=v --incrementer=MINOR --postfix=RELEASE`

Result: `v1.2.4.RELEASE`

**Scenario 5:**

From: `v1.2.4.RELEASE`

Config: `vertere init --prefix=v --incrementer=MINOR --postfix=RELEASE`

Result: `v1.3.0.RELEASE`

**Scenario 6:**

From: `v1.2.4.RELEASE`

Config: `vertere init --prefix=v --incrementer=MINOR`

Result: `v1.3.0`

### CLI Properties
```
vertere --help

Usage: vertere [OPTIONS] [ init | push | read ]

Options:

--initial-version TEXT 
Required when a project has not been yet initialised. 
It will determine the initial version for a git project. 
Default value: 1.0.0

--prefix TEXT
Optional property that sets a prefix for a version. 
Default value: '' (empty string)
Example.: when --prefix=v, the version will be displayed as v1.2.3

--incrementer [ PATCH | MINOR | MAJOR]
Value that dictates how the next version will be incremented. 
Default value: PATCH

--postfix TEXT
Optional property that can be used to append a known postfix to the version.
It supports [BUILD-SNAPSHOT, M, RC and RELEASE].
Example: --postfix=RELEASE, the next version will be displayed as 1.2.3.RELEASE. 

--config-path TEXT
Optional property, used to point to vertere file configuration.
Default value: vertere.yml

--debug BOOLEAN 
Enables extra log lines while executing this program. 
it might help to identify a possible problem. 
Default value: false

 ```

### File configuration

This CLI program can have the properties persisted in the git project. 
by default, it tries to load `vertere.yml`

File format example:

```yaml
versioning:
  initial-version: 1.0.0.BUILD-SNAPSHOT
  prefix: v
  postfix: BUILD-SNAPSHOT | M | RC | RELEASE
  incrementer: MAJOR | MINOR | PATCH
```
