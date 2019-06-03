import click
from click.testing import CliRunner
from  kcleaner import cli
from testfixtures import log_capture


runner = CliRunner()

@log_capture()
def test_clean_non_existant_file(capture):
    
    results = runner.invoke(cli, ['-k', './non_existent_file'])
    assert results.exit_code == 10
    capture.check_present(
        ('root', 'DEBUG', 'Trying to retrieve contents of file ./non_existent_file'),
        ('root', 'DEBUG', 'checking if file ./non_existent_file exists...'),
        ('root', 'INFO', 'Config File Not found!'),
        ('root', 'ERROR', 'Cannot work with an empty file!, please check the path of your config file.'),
    )

@log_capture()
def test_clean_empty_file(capture):
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('')

        result = runner.invoke(cli, ['-k', './config'])
        assert result.exit_code == 11
        capture.check_present(
            ('root', 'DEBUG', 'Trying to retrieve contents of file ./config'),
            ('root', 'DEBUG', 'checking if file ./config exists...'),
            ('root', 'DEBUG', 'File exists!'),
            ('root', 'DEBUG', "Type of the file contents: <class 'NoneType'>"),
            ('root', 'ERROR', "Config File is empty! Can't use it.")
        )

@log_capture()
def test_clean_empty_file_debug(capture):
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('')

        result = runner.invoke(cli, ['-k', './config', '-d'])
        assert result.exit_code == 11
        capture.check_present(
            ('root', 'DEBUG', 'Running with Debug flag'),
            ('root', 'DEBUG', 'Trying to retrieve contents of file ./config'),
            ('root', 'DEBUG', 'checking if file ./config exists...'),
            ('root', 'DEBUG', 'File exists!'),
            ('root', 'DEBUG', "Type of the file contents: <class 'NoneType'>"),
            ('root', 'ERROR', "Config File is empty! Can't use it.")
        )

@log_capture()
def test_clean_empty_file_undo(capture):
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('')

        result = runner.invoke(cli, ['-k', './config', '-u'])
        #assert result.exit_code == 11
        capture.check_present(
            ('root', 'INFO', 'Undo flag was set! checking for the backup file...')
        )

@log_capture()
def test_non_valid_yaml(capture):
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('lololol')

        result = runner.invoke(cli, ['-k', './config'])
        assert result.exit_code == 12
        capture.check_present(
            ('root', 'DEBUG', 'checking if file ./config exists...'),
            ('root', 'DEBUG', 'File exists!'),
            ('root', 'ERROR', 'Config File is not a valid yaml file!'),
        )