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

nodejs_repository: ppa:chris-lea/node.js  # NodeJS PPA
nodejs_npm_modules: []                    # List modules which will be installed
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
