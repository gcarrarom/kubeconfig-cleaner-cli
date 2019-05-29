from  kcleaner import update_file
from testfixtures import log_capture
import click
from click.testing import CliRunner
import pytest
import yaml

runner = CliRunner()
sample_yaml = """
something:
  alist:
  - item1: test
    something: test
  - item2: test
    something: test
"""

@log_capture()
def test_none_parameters(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        update_file(None, None)

    assert pytest_wrapped_e.value.code == 20
    capture.check_present(
        ('root', 'ERROR', "Filename cannot be 'None'")
    )

@log_capture()
def test_none_file_empty_content(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        update_file(None, "")

    assert pytest_wrapped_e.value.code == 20
    capture.check_present(
        ('root', 'ERROR', "Filename cannot be 'None'")
    )

@log_capture()
def test_empty_file_empty_content(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        update_file("", "")

    assert pytest_wrapped_e.value.code == 21
    capture.check_present(
        ('root', 'ERROR', 'Filename cannot be empty!')
    )

@log_capture()
def test_non_existant_file_none_content(capture):
    with runner.isolated_filesystem():
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            update_file("./config", None)

        assert pytest_wrapped_e.value.code == 30
        capture.check_present(
            ('root', 'ERROR', "Yaml Value cannot be 'None'!")
        )

@log_capture()
def test_non_existant_file_empty_content(capture):
    with runner.isolated_filesystem():
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            update_file("./config", "")

        assert pytest_wrapped_e.value.code == 31
        capture.check_present(
            ('root', 'ERROR', 'Yaml Value cannot be empty!')
        )

@log_capture()
def test_non_existant_file_not_yaml_content(capture):
    with runner.isolated_filesystem():
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            update_file("./config", "{{123lololol123}}")

        assert pytest_wrapped_e.value.code == 32
        capture.check_present(
            ('root', 'ERROR', 'Yaml value is not valid!')
        )

@log_capture()
def test_existant_file_yaml_content(capture):
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('lololol')
        update_file("./config", sample_yaml)

        with open('./config', 'r') as f:
            result = yaml.safe_load(f)

        assert sample_yaml in result
        capture.check_present(
            ('root', 'DEBUG', 'Writing new yaml doc into the config file')
        )