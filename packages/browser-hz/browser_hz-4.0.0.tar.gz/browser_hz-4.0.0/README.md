# Browser

[<img src="https://img.shields.io/badge/releases-PyPI-blue">](https://pypi.org/project/browser-hz/)

## Background

This project was initiated with the aim of comprehending the fundamental workings of Python packages, their
distribution, and the process of releasing them using the project and dependency management tool, Poetry.
The package was developed for internal utilization across various Python projects such
as [browser-network-interception](https://github.com/hubzaj/browser-network-interception).
Its primary objective is to facilitate an in-depth understanding of package management while serving as a valuable asset
for diverse Python projects.

### How to build project

Requirements:

-     Python ^3.11
-     Poetry ^1.5.1

### Working with terminal

1. Install `asdf` with required plugins.

 ```
  > brew install asdf
  > asdf plugin-add python
  > asdf plugin-add poetry
  > asdf install
 ```

### Configuration

Configuration is designed in a way to be controlled by environment variables.

    [BROWSER]

##### Default:

* Browser: `Chrome (without headless)`

#### Supported browsers:

* `CHROME`
* `CHROME_HEADLESS`
* `CHROME_IN_DOCKER` [NOT READY YET]

