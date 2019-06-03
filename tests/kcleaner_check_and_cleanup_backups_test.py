from  kcleaner import check_and_cleanup_backups, backup_limit
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
        check_and_cleanup_backups(None)

    assert pytest_wrapped_e.value.code == 40
    capture.check_present(
        ('root', 'ERROR', "Filename cannot be 'None'!")
    )

@log_capture()
def test_bellow_backup_limit(capture):
    with runner.isolated_filesystem():

        for i in range(backup_limit-1):
            with open(f'./something_{i}_kcleaner.bak', 'w') as f:
                f.write('lololol')

        check_and_cleanup_backups("./something")

        capture.check_present(
            ('root', 'DEBUG', 'We are bellow the backup limit, nothing to do here.')
        )

@log_capture()
def test_1_over_backup_limit(capture):
    with runner.isolated_filesystem():

        for i in range(backup_limit+1):
            with open(f'./something_{i}_kcleaner.bak', 'w') as f:
                f.write('lololol')

        check_and_cleanup_backups("./something")

        capture.check_present(
            ('root', 'DEBUG', 'Removing File something_0_kcleaner.bak')
        )

@log_capture()
def test_2_over_backup_limit(capture):
    with runner.isolated_filesystem():

        for i in range(backup_limit+2):
            with open(f'./something_{i:03}_kcleaner.bak', 'w') as f:
                f.write('lololol')

        check_and_cleanup_backups("./something")

        capture.check_present(
            ('root', 'DEBUG', 'Removing File something_000_kcleaner.bak'),
            ('root', 'DEBUG', 'Removing File something_001_kcleaner.bak')
        )