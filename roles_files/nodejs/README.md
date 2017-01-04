Stouts.nodejs
=============

[![Build Status](http://img.shields.io/travis/Stouts/Stouts.nodejs.svg?style=flat-square)](https://travis-ci.org/Stouts/Stouts.nodejs)
[![Galaxy](http://img.shields.io/badge/galaxy-Stouts.nodejs-blue.svg?style=flat-square)](https://galaxy.ansible.com/list#/roles/983)

Ansible role which manage nodejs and npm packages.

#### Requirements

Only tested on ubuntu for now.

#### Variables

```yaml
nodejs_enabled: yes                       # The role is enabled
nodejs_version: 5.9.0
nodejs_major_version: 5.x                 # This will determine the repo from nodejs.org used
nodejs_install: pkg                       # Install nodejs from packages, sources or binary
                                          # (pkg|src|bin)

nodejs_npm_modules: []                    # List modules which will be installed

nodejs_home: /usr/lib/nodejs              # The directory where nodejs will be installed
nodejs_src_url: "http://nodejs.org/dist/v{{nodejs_version}}/node-v{{nodejs_version}}.tar.gz"
nodejs_bin_url: "http://nodejs.org/dist/v{{nodejs_version}}/node-v{{nodejs_version}}-{{ansible_system|lower}}-x{{ansible_userspace_bits|replace('32', '86')}}.tar.gz"
```

#### Usage

Add `Stouts.nodejs` to your roles and set vars in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.nodejs

  vars:
    nodejs_npm_modules:
      - bower
      - jshint
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.nodejs/issues)!

If you wish to express your appreciation for the role, you are welcome to send
a postcard to:

    Kirill Klenov
    pos. Severny 8-3
    MO, Istra, 143500
    Russia
