from __future__ import print_function
from  kcleaner import ask_yn
import kcleaner
from testfixtures import log_capture
import click
from click.testing import CliRunner
import pytest
import yaml
from io import StringIO
import json

runner = CliRunner()

@log_capture()
def test_ask_yn_more_than_2_wrong_answers(capture, monkeypatch):
    with runner.isolated_filesystem():
        number_inputs = StringIO('a\na\na\na\n')
        monkeypatch.setattr('sys.stdin', number_inputs)

        response = ask_yn("some question")
                
        assert response == 'n'


@log_capture()
def test_ask_yn_1_wrong_and_1_right_answer(capture, monkeypatch):
    with runner.isolated_filesystem():
        number_inputs = StringIO('a\ny\n')
        monkeypatch.setattr('sys.stdin', number_inputs)

        response = ask_yn("some question")
                
        assert response == "y"

