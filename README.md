Ansible role: docker
====================
[![Build Status](https://travis-ci.org/apkawa/ansible-role-docker.svg?branch=master)](https://travis-ci.org/apkawa/ansible-role-docker)

[![Ansible role](https://img.shields.io/ansible/role/42615.svg)](https://galaxy.ansible.com/apkawa/docker)
[![Ansible role downloads](https://img.shields.io/ansible/role/d/42615.svg)](https://galaxy.ansible.com/apkawa/docker)
[![Ansible role quality](https://img.shields.io/ansible/quality/42615.svg)](https://galaxy.ansible.com/apkawa/docker)

Ansible role for installation `docker`, `docker-compose` and optional `ctop`

Requirements
------------

None

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):
```yaml
docker_storage_driver: overlay2
docker_config_file: "/etc/docker/daemon.json"
docker_data_root: "/var/lib/docker"
docker_config_dns:
  - 8.8.8.8
  - 8.8.4.4

# https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file
# Overrides in daemon.json format
docker_daemon_opts:
  data-root: /opt/docker/
  label:
    - foo=bar
    - key=value
  dns: 
      - 8.8.8.8
      - 8.8.4.4
    


# Debian/Ubuntu: apt-cache madison docker-ce  
# CentOS/Fedora: yum list docker-ce --showduplicates | sort -r
# By default - fill from variable by avtodetection OS
docker_version: null

# Login to registry
docker_registry:
   # For full options - see https://docs.ansible.com/ansible/latest/modules/docker_login_module.html
 - registry: registry.gitlab.com
   username: apkawa
   password: !vault |
     $ANSIBLE_VAULT;1.1;AES256

# docker_compose
docker_compose: yes
docker_compose_bin: /usr/local/bin/docker-compose
# https://github.com/docker/compose/releases
docker_compose_version: 1.24.1
docker_compose_checksum: "sha256:cfb3439956216b1248308141f7193776fcf4b9c9b49cbbe2fb07885678e2bb8a"
docker_compose_release_url: "https://github.com/docker/compose/releases/download/{{ docker_compose_version }}/docker-compose-Linux-x86_64"

# ctop
docker_ctop: no
docker_ctop_bin: /usr/local/bin/ctop
docker_ctop_version: 0.7.2
docker_ctop_checksum: "sha256:e1af73e06f03caf0c59ac488c1cda97348871f6bb47772c31bbd314ddc494383"
docker_ctop_release_url: "https://github.com/bcicen/ctop/releases/download/v/ctop-{{ docker_ctop_version }}-linux-amd64"
```

### Swarm mode

```yaml
docker_swarm_enabled: yes

# Host variables
# Must be one!
docker_swarm_master: no
# Host with manager
docker_swarm_manager: no
# Host swarm worker
docker_swarm_worker: no

# Optional
docker_swarm_listen_addr: '0.0.0.0:2377'
docker_swarm_advertise_addr: "{{ ansible_default_ipv4.interface }}"
docker_swarm_remote_addr: "{{ ansible_default_ipv4.address }}:2377"
```

https://docs.docker.com/engine/swarm/

### Consul

For enable consul cluster store without swarm

```yaml
# Experimental!
# Consul

docker_consul_enabled: yes
# Node with consul store. Must be one
docker_consul_server_ui: no
docker_consul_server: no
docker_consul_agent: no
# Optional
# ethernet device or ip. by default - "{{ host.ansible_default_ipv4.address }}"
docker_consul_bind: null # eth0 | 10.0.1.5
# by default - consul agent every nodes
docker_consul_store_address: localhost

# Version tag from https://hub.docker.com/_/consul?tab=tags
docker_consul_version: 1.5
```


Useful links 

* https://www.consul.io/
* https://luppeng.wordpress.com/2016/05/03/setting-up-an-overlay-network-on-docker-without-swarm/
* https://hub.docker.com/r/_/consul/

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: all
  roles:
    - role: apkawa.docker
```

License
-------

MIT 

Author Information
------------------

Apkawa 


Contributing
------------

1. [Install docker](https://docs.docker.com/install/linux/docker-ce/debian/)
2. [Install tox](https://tox.readthedocs.io/en/latest/install.html)
2. Run tests
    ``` 
    tox -e centos7
    ```
   
###  Low level run part of test

1. pipenv shell
2. `molecule converge` 
3. `molecule idempotence`
4. `molecule verify` for run Testinfra
