# lfsData

<p align="center">
  <a href="https://pypi.org/project/lfsdata"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/lfsdata.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/lfsdata"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/lfsdata.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/lfsdata"><img alt="License" src="https://img.shields.io/pypi/l/lfsdata.svg?maxAge=86400" /></a>
  <a href="https://github.com/arushadev/lfsdata/actions/workflows/pylint.yml"><img alt="Pylint" src="https://github.com/arushadev/piraye/actions/workflows/pylint.yml/badge.svg" /></a>
  <a href="https://github.com/arushadev/lfsdata/actions/workflows/unit-test.yml/badge.svg)](https://github.com/arushadev/piraye/actions/workflows/unit-test.yml"><img alt="Unit Test" src="https://github.com/arushadev/piraye/actions/workflows/unit-test.yml/badge.svg" /></a>
</p>
This document provides instructions on how to work with Git Large File Storage (LFS) for the `qomnet` project.

## Getting Started with Git LFS

Git LFS is a Git extension that improves handling of large files by replacing them with text pointers inside Git, while
storing the file content on a remote server.

## Downloading single file

Before execution of this script, create an access token with `read_api` capability and set it as an Environment Variable
for `GITLAB_ACCESS_TOKEN`. Here's how, depending on your operating system: ([Gitlab token creation
tutorial](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html))

- On Windows:

``` shell
$env:GITLAB_ACCESS_TOKEN="your_access_token_here"
```

- On Linux:

``` shell
export GITLAB_ACCESS_TOKEN="your_access_token_here"
```

It's also possible to set this variable in PyCharm. Check out
this [tutorial](https://stackoverflow.com/questions/42708389/how-to-set-environment-variables-in-pycharm/42708480#42708480)
for guidance.

Once you've set the `GITLAB_ACCESS_TOKEN`, you can download a file using the following Python function, which includes
these parameters:

- `host`: The domain from which we want to download the dataset
- `id`: The ID of the desired repository, which can be found on the first page of each repository
- `branch_name`: The name of the branch where the desired file or data is stored
- `file_path`: The address of the desired file in the repository

``` python
DataLoader().gitlab_download("https://git.arusha.dev", 123, "branch_name", "data/test.gz")
```

Executing this command initiates the file download process, which is accompanied by a progress bar. The downloaded file
is placed in the HOME directory, at: .local/datasets/{project_id}/{branch_name}/{file_path}.
You can locate your home directory path based on your operating system:

| Operating system |        Path         |
|:----------------:|:-------------------:|
|     Windows      | C:\Users\<username> |
|      Linux       |  /home/<username>   |
|      macOS       |  /Users/<username>  |

In addition, you might find this tutorial about LFS very helpful.

### Installation

To install Git LFS, use the following command:

``` shell
git lfs install
```

## Clone Repository

To clone repository with only pointer files, use following commands:

* Linux (bash):

``` shell
GIT_LFS_SKIP_SMUDGE=1 git clone ssh://git@git.arusha.dev:9022/majd/datasets/qomnet.git
```

* Windows:

``` shell
$env:GIT_LFS_SKIP_SMUDGE="1"
git clone ssh://git@git.arusha.dev:9022/majd/datasets/qomnet.git
``` 

## Tracking Files :

``` shell
git lfs track "*.psd"
git add .gitattributes
```

## Committing & Pushing Changes :

To commit and push changes, type:

``` shell
git add file.psd
git commit -m "Add design file"
git push origin main
```

For more information about Git LFS, check [here](https://git-lfs.com/)