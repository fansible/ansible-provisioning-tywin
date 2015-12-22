# ansible-role-composer

[![License](https://img.shields.io/badge/License-MIT%20License-blue.svg)](https://github.com/kosssi/ansible-role-composer/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/kosssi/ansible-role-composer.svg?branch=master)](https://travis-ci.org/kosssi/ansible-role-composer)

Installs Composer, the PHP Dependency Manager.

## Role Defaults Variables

    composer_path: /usr/local/bin/composer
    composer_update: true
    composer_update_day: 20

The path where composer will be installed and available to your system. Should be in your user's `$PATH` so you can run
commands simply with `composer` instead of the full path.

You can also setup a global composer directory and make the bin directory available in the `$PATH` automatically by:
 
    composer_path_env: true
    composer_home_path: /opt/composer
    composer_home_owner: root
    composer_home_group: root
    composer_global_packages:
      phpunit/phpunit: "@stable"

If your project use a lot of libraries from github, you may see next message during `composer install`:

    Could not fetch `...`, enter your GitHub credentials to go over the API rate limit
    A token will be created and stored in "~/.composer/auth.json", your password will never be stored
    To revoke access to this token you can visit https://github.com/settings/applications

So your `composer install` can get stuck.

To prevent that, you must configure github oauth token to go over the API rate limit. Visit https://github.com/settings/applications and generate personal access token and assign it to `composer_github_oauth` variable.

    composer_github_oauth: f03401aae1e276abb073f987c08a32410f462e73

## Example Playbook

      roles:
        - { role: kosssi.composer }

## Tests

If you have vagrant, you can test this role:

    cd tests
    vagrant up
    vagrant provision

## Special thanks to contributors

* [jnakatsui](https://github.com/jnakatsui)
* [Yosh](https://github.com/yoshz)
* [Johnny Robeson](https://github.com/jrobeson)
* [Sebastian Krebs](https://github.com/KingCrunch)
