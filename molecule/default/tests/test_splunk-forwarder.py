import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_splunk_group_exists(host):
    splunk_group = host.group("splunk")
    assert splunk_group.exists


def test_splunk_user_exists(host):
    splunk_user = host.user("splunk")
    assert splunk_user.exists
