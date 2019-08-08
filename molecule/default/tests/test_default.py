import json
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_info(host):
    cmd = host.run('docker info')
    assert cmd.rc == 0
    assert "Storage Driver: vfs" in cmd.stdout
    assert "Docker Root Dir: /opt/docker" in cmd.stdout


def test_docker_compose(host):
    cmd = host.run('docker-compose --version')
    assert cmd.rc == 0
    assert "docker-compose version 1.24.1" in cmd.stdout


def test_daemon_json(host):
    f = host.file('/etc/docker/daemon.json')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert json.loads(f.content_string) == {
        "dns": [
            "8.8.8.8",
            "8.8.4.4"
        ],
        "storage-driver": "vfs",
        "data-root": "/opt/docker/"
    }
