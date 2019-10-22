![GitHub release](https://img.shields.io/github/release/gcarrarom/kubeconfig-cleaner-cli.svg)
[![Master Build Status](https://dev.azure.com/FancyWhale/FancyWhale/_apis/build/status/kcleaner%20CI?branchName=master)](https://dev.azure.com/FancyWhale/FancyWhale/_build/latest?definitionId=2&branchName=master)
# Table of contents
- [Table of contents](#table-of-contents)
- [Demo](#demo)
- [Usage](#usage)
- [Installation](#installation)
  - [PyPI (pip)](#pypi-pip)
  - [PyPI Test](#pypi-test)
- [TO-DO](#to-do)


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
There are plenty of ways of installing this tool. Although I would always recommend to wait for the full release, feel free to download the beta versions as well.
## Requirements
Python 3.x
## PyPI (pip)
To install using pip, simply run this command:

`pip install kcleaner`
## PyPI Test
This is the first distribution place for the tool, latest version might not be fully operational

`pip install -i https://test.pypi.org/simple/ kcleaner`

# TO-DO

- [ ] Automated publishing to PyPI, Brew and Chocolatey
  - [x] Automated release to PyPI Test
  - [x] Automated release to PyPI
  - [ ] Automated release to Brew
  - [ ] Automated release to Chocolatey
- [x] Add more tests, Code coverage is laughable now ;)
- [x] Add undo flag... Life happens ¯\\\_(ツ)\_/¯
- [x] ~~Make it easier to add changes and modules to the tool - Changed to use command group instead~~ Not worth it.
