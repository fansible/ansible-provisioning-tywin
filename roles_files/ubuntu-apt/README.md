kosssi.apt
==========

[![Build Status](https://travis-ci.org/kosssi/ansible-role-apt.svg?branch=master)](https://travis-ci.org/kosssi/ansible-role-apt)

Ansible role for execute apt-get update and install apt-repositories and apt-packages.

Role Defaults Variables
-----------------------

See [defaults/main.yml](defaults/main.yml) for more information.

    apt_cache_valid_time: 3600
    apt_upgrade: true
    apt_upgrade_type: safe          # safe, full or dist
    apt_install:
      - python-apt
      - unattended-upgrades
    apt_install_repositories: false
    apt_remove_repositories: false

Example Playbook
----------------

    - hosts: localhost
      vars:
          apt_install: [cowsay, cowthink, sl, figlet]
      roles:
        - { role: kosssi.apt, tags: apt }

License
-------

Licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
