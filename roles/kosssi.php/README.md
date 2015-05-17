# ansible-role-php

[![Build Status](https://travis-ci.org/kosssi/ansible-role-php.svg?branch=master)](https://travis-ci.org/kosssi/ansible-role-php)

Install and configure PHP

## Role Defaults Variables

    php_repository: false
    php_timezone: Europe/Paris

    php_install:
      - php5

    php_configure:
      - file: /etc/php5/cli/php.ini
        values:
          - { section: date, key: date.timezone, value: '{{ php_timezone }}' }
      - file: /etc/php5/apache2/php.ini
        values:
          - { section: date, key: date.timezone, value: '{{ php_timezone }}' }

## Exemple of configuration role

    php_repository: ppa:ondrej/php5
    php_install:
      - php5
      - php5-xdebug
    php_configure:
      - file: /etc/php5/cli/php.ini
        values:
          - { section: date, key: date.timezone, value: '{{ php_timezone }}' }
      - file: /etc/php5/mods-available/xdebug.ini
        values:
          - { section: date, key: date.timezone, value: '{{ php_timezone }}' }
          - { section: xdebug, key: xdebug.idekey, value: my-idekey }

## Example Playbook

    roles:
      - { role: kosssi.php, tags: php }

## License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
