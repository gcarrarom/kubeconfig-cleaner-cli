from  kcleaner import cli
from testfixtures import log_capture
import click
from click.testing import CliRunner
import pytest
import yaml

#cli(resource, name, kubeconfig, undo, debug)

runner = CliRunner()
sample_yaml = """
something:
  alist:
  - item1: test
    something: test
  - item2: test
    something: test
"""
