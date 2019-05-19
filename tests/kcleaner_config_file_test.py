import click
from click.testing import CliRunner
from  kcleaner import cli

runner = CliRunner()
def test_clean_non_existant_file():
    
    results = runner.invoke(cli, ['-k', './non_existent_file'])

    assert results.exit_code == 10
    assert 'Config File Not found!' in results.output

def test_clean_empty_file():
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('')

        result = runner.invoke(cli, ['-k', './config'])
        assert result.exit_code == 11
        assert "Config File is empty! Can't use it." in result.output

def test_non_valid_yaml():
    with runner.isolated_filesystem():
        with open('./config', 'w') as f:
            f.write('lololol')

        result = runner.invoke(cli, ['-k', './config'])
        assert result.exit_code == 12
        assert "Config File is not a valid yaml file!" in result.output