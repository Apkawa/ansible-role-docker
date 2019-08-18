# flake8: noqa
import json
import os

import testinfra.utils.ansible_runner

RUNNER = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE'])

testinfra_hosts = RUNNER.get_hosts('all')

worker = RUNNER.get_host('instance-consul-worker')

master = RUNNER.get_host('instance-consul-master')


def test_docker_info(host):
    cmd = host.run('docker info')
    assert cmd.rc == 0
    assert "Storage Driver: vfs" in cmd.stdout
    assert "Docker Root Dir: /opt/docker" in cmd.stdout
    assert f"Cluster Store: " in cmd.stdout
    assert f"Cluster Advertise: " in cmd.stdout


def test_docker_compose(host):
    cmd = host.run('docker-compose --version')
    assert cmd.rc == 0
    assert "docker-compose version 1.24.1" in cmd.stdout


def test_network_overlay():
    master.run('docker rm -f container_master')
    worker.run('docker rm -f container_worker')
    master.run('docker network rm test_overlay_master test_overlay_worker')
    worker.run('docker network rm test_overlay_master test_overlay_worker')
    assert master.run(
        'docker network create -d overlay test_overlay_master').rc == 0
    assert worker.run(
        'docker network create -d overlay test_overlay_worker').rc == 0

    assert master.run(
        'docker run -itd --net test_overlay_master --name container_master busybox').rc == 0
    assert worker.run(
        'docker run -itd --net test_overlay_worker --name container_worker busybox').rc == 0

    assert worker.run(
        'docker run --rm --net test_overlay_master busybox ping -c 3 container_master').rc == 0
    assert master.run(
        'docker run --rm --net test_overlay_worker busybox ping -c 3 container_worker').rc == 0


def test_daemon_json(host):
    f = host.file('/etc/docker/daemon.json')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

    config = json.loads(f.content_string)
    # problem get current ip
    del config['cluster-store']
    assert config == {
        "dns": [
            "8.8.8.8",
            "8.8.4.4"
        ],
        "storage-driver": "vfs",
        "data-root": "/opt/docker/",
        "hosts": [
            "tcp://0.0.0.0:2377",
            "unix:///var/run/docker.sock"
        ],
        "cluster-advertise": "eth0:2377",
    }
