from __future__ import print_function
from  kcleaner import remove_resource, get_file
from testfixtures import log_capture
import click
from click.testing import CliRunner
import pytest
import yaml
from mock import patch

runner = CliRunner()
sample_yaml_no_token = """
apiVersion: v1
clusters:
- cluster:
    server: https://super.coolcluster.fancywhale.ca
  name: SuperCoolCluster
contexts:
- context:
    cluster: SuperCoolCluster
    user: SuperCoolUserName
  name: SuperCoolContext1
current-context: SuperCoolContext
kind: Config
preferences: {}
users:
- name: SuperCoolUserName1
  user:
    auth-provider:
      config:
        apiserver-id: some-id-that-makes-sense
        client-id: some-id-that-makes-sense
        tenant-id: some-id-that-makes-sense
      name: some-auth-provider
"""
sample_yaml_token = """
apiVersion: v1
clusters:
- cluster:
    server: https://super.coolcluster.fancywhale.ca
  name: SuperCoolCluster
contexts:
- context:
    cluster: SuperCoolCluster
    user: SuperCoolUserName
  name: SuperCoolContext1
current-context: SuperCoolContext
kind: Config
preferences: {}
users:
- name: SuperCoolUserName1
  user:
    auth-provider:
      config:
        access-token: SomeRandomToken
        apiserver-id: some-id-that-makes-sense
        client-id: some-id-that-makes-sense
        expires-in: '3600'
        expires-on: '1559593884'
        refresh-token: SomeRandomRefreshToken
        tenant-id: some-id-that-makes-sense
      name: some-auth-provider
"""

@log_capture()
def test_none_parameters(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        remove_resource(None, None)

    assert pytest_wrapped_e.value.code == 50
    capture.check_present(
        ('root', 'ERROR', 'Config File cannot be "None"!'),
    )

@log_capture()
def test_removing_type_none(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        remove_resource("", None)

    assert pytest_wrapped_e.value.code == 50
    capture.check_present(
        ('root', 'ERROR', 'Removing type cannot be "None"!'),
    )

@log_capture()
def test_config_file_empty(capture):
    
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        remove_resource("", "")

    assert pytest_wrapped_e.value.code == 51
    capture.check_present(
        ('root', 'ERROR', 'Parameters cannot be empty!'),
    )

""" @log_capture()
@patch('kcleaner.iterfzf')
def test_remove_token_not_available(capture, test_patch):
    with runner.isolated_filesystem():

        with open(f'./SampleConfigFile', 'w') as f:
                f.write(sample_yaml_no_token)

        config_file = get_file("./SampleConfigFile")

        test_patch.return_value = ""

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            new_config = remove_resource(config_file, "token")
        
        assert pytest_wrapped_e.value.code == 52
        capture.check_present(
            ('root', 'ERROR', 'No resources to remove selected!'),
        ) """

""" @log_capture()
@patch('kcleaner.iterfzf')
def test_remove_token(test_patch, capture):
    name_to_remove = "SuperCoolUserName1"
    with runner.isolated_filesystem():

        with open(f'./SampleConfigFile', 'w') as f:
            f.write(sample_yaml_token)
        with open(f'./SampleConfigFileToTest', 'w') as f:
            f.write(sample_yaml_no_token)

        config_file = get_file("./SampleConfigFile")
        config_to_test = get_file("./SampleConfigFileToTest")

        test_patch.return_value = f"{name_to_remove}"

        new_config = remove_resource(config_file, "token")
        
        assert new_config == config_to_test
        capture.check_present(
            ('root', 'DEBUG', f'Removing token information from the user(s) {name_to_remove}'),
            ('root', 'DEBUG', f'removing tokens from user {name_to_remove}'),
            ('root', 'DEBUG', 'Token Removed successfully!'),
        ) """