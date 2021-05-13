![GitHub release](https://img.shields.io/github/release/gcarrarom/kubeconfig-cleaner-cli.svg)
[![codecov](https://codecov.io/gh/gcarrarom/kubeconfig-cleaner-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/gcarrarom/kubeconfig-cleaner-cli)
![PyPI - Downloads](https://img.shields.io/pypi/dm/kcleaner) 
# Table of contents
- [Table of contents](#table-of-contents)
- [Demo](#demo)
- [Usage](#usage)
- [Installation](#installation)


# Demo
I want to clean my Kube config file without having to open my config file ever again :)

<p align="center">
  <img src="https://github.com/gcarrarom/kubeconfig-cleaner-cli/raw/master/render1557878856917.gif">
</p>


# Usage

To use this CLI simply type:
`kcleaner`
This will prompt you to remove the context by using Fuzzy Search.
If you want to clean another Kube config file, you should use the option `-k` or `--kube-config` with the path for your config file.
If you want to remove clusters, you can too! Just call `kcleaner clusters` and voilá!
What about users? Sure can! `kcleaner users` is here to help!
To select more than one entry, just press tab. All the selected entries will be removed!

If you know the name of the config entry you're going to remove, you can always use the `-n` or `--name` option to remove it.

Here's the output of the help command `kcleaner --help`:
```
Usage: kcleaner.py [OPTIONS] [[users|clusters|contexts|token]]

  A little CLI tool to help keeping Config Files clean :)

Options:
  -k, --kubeconfig TEXT  path to the config file to clean
  -n, --name TEXT        Name of the entry to remove
  -u, --undo             Use this to roll back latest changes
  -d, --debug            Use this to see debug level messages
  --help                 Show this message and exit.
```

# Installation

To install using pip, simply run this command:

`pip install kcleaner`

## Requirements
Python 3.x
