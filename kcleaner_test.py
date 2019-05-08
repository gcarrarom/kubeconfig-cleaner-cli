import click
from click.testing import CliRunner
from  kcleaner import main

runner = CliRunner()
def test_clean_non_existant_file():
    
    results = runner.invoke(main, ['-k', './non_existent_file', '-m', 'context'])

    assert results.exit_code == 10
    assert 'Config File Not found!' in results.output

def test_clean_empty_file():
    with runner.isolated_filesystem():
        with open('config', 'w') as f:
            f.write('')

        result = runner.invoke(main, ['-k', './config'])
        assert result.exit_code == 11
        assert "Config File is empty! Can't use it." in result.output

def test_non_valid_yaml():
    with runner.isolated_filesystem():
        with open('config', 'w') as f:
            f.write('{"name":"randomJson"}')

        result = runner.invoke(main, ['-k', './config'])
        assert result.exit_code == 11
        assert "Config File is not a valid yaml file!" in result.output
