# flake8: noqa
import json
import os

import testinfra.utils.ansible_runner

RUNNER = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE'])

testinfra_hosts = RUNNER.get_hosts('all')

worker = RUNNER.get_host('instance-swarm-worker')

master = RUNNER.get_host('instance-swarm-master')


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
        "data-root": "/opt/docker/",
        'hosts': [
            'unix:///var/run/docker.sock'
        ]
    }


def test_swarm_nodes():
    cmd = master.run('docker node ls')
    assert cmd.rc == 0
    assert "instance-swarm-master" in cmd.stdout
    assert "instance-swarm-worker" in cmd.stdout

    cmd = master.run('docker node inspect instance-swarm-master')
    assert cmd.rc == 0
    assert json.loads(cmd.stdout)[0]['ManagerStatus']['Leader']
    assert json.loads(cmd.stdout)[0]['Status']['State'] == 'ready'

    cmd = master.run('docker node inspect instance-swarm-worker')
    assert cmd.rc == 0
    assert json.loads(cmd.stdout)[0]['Status']['State'] == 'ready'


def test_swarm_deploy():
    master.run("docker service rm test_swarm").rc
    assert master.run(
        'docker service create --name test_swarm --replicas=2 busybox ping ya.ru').rc == 0

    cmd = master.run("docker service ps test_swarm")
    assert cmd.rc == 0
    assert 'instance-swarm-master' in cmd.stdout
    assert 'instance-swarm-worker' in cmd.stdout

    assert master.run("docker service rm test_swarm").rc == 0
