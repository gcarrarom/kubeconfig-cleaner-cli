from  kcleaner import file_exists
from testfixtures import log_capture
import click
from click.testing import CliRunner
import pytest

runner = CliRunner()

@log_capture()
def test_no_parameters(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        file_exists(None)

    assert pytest_wrapped_e.value.code == 20
    capture.check_present(
        ('root', 'ERROR', "Filename cannot be 'None'")
    )

@log_capture()
def test_empty_string(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        file_exists("")

    assert pytest_wrapped_e.value.code == 21
    capture.check_present(
        ('root', 'ERROR', "Filename cannot be empty!")
    )

@log_capture()
def test_existing_file(capture):
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('lololol')

        exists = file_exists("./config")

        assert exists == True
        capture.check_present(
            ('root', 'DEBUG', 'File exists!')
        )

@log_capture()
def test_non_existing_file(capture):
    with runner.isolated_filesystem():

        exists = file_exists("./config")

        assert exists == False
        capture.check_present(
            ('root', 'INFO', 'Config File Not found!')
        )

