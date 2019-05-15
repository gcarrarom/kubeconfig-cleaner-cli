# kcleaner
![GitHub release](https://img.shields.io/github/release/gcarrarom/kubeconfig-cleaner-cli.svg)
[![Master Build Status](https://dev.azure.com/FancyWhale/FancyWhale/_apis/build/status/kcleaner%20CI?branchName=master)](https://dev.azure.com/FancyWhale/FancyWhale/_build/latest?definitionId=2&branchName=master)

I want to clean my kube config file without having to open my config file ever again :)

<p align="center">
  <img src="https://github.com/gcarrarom/kubeconfig-cleaner-cli/raw/master/render1557878856917.gif">
</p>

# Usage

To use this CLI simply type:
`kcleaner`
This will prompt you to remove the context by using Fuzzy Search.
If you want to clean another kube config file, you should use the flag `-k` or `--kube-config` with the path for your config file

# Versions and Branches
The naming of the branches are important as the versioning is automatic.
```
v$(majorVersion).$(devVersion).$(betaVersion)
```
## Master
Any new Pull Requests to Master are going to increase the master version by 1.
If on version `v0.2.1` and pushed to master, the new release is going to be `v1.0.0`.
## Dev
The dev branches should be created following the pattern of the version of the master branch you are working on.
If you are working out of the version `v1.0.0`, the dev branch should be named `dev/1`, the pipelines will then understand that you are developing in the version v1 and every commit/PR to this branch will then release a new version.
If working on version `v1.0.1` and pushed to `dev/1`, the new release is going to be `v1.1.0`
## Beta
Following the same pattern as Dev, beta branches are going to follow the same naming scheme: `beta/1.0`.
If working on version `v1.2.3` and pushed to `beta/1.2`, the new release is going to be `v1.2.4`
