# nginx-main-conf role for Ansible
Install a main conf file taht listen to *.subconf files for partial configurations

## Set up
- Add this role and eventually it's dependencies in your `roles` folder as git submodule:
`git submodule add git://github.com/davinov/ansible-nginx-main-conf [path-to-roles]/nginx-main-conf`
- Add it to your playbook's roles if it's not required by another one

## Variables
`domain` default to `_`
