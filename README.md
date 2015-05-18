# Fansible Tywin
Create easily your Ansible provisioning

## Still WIP
This is still under development: it is not a reliable repository yet

## How to use it

### Installation

    composer require fansible/tywin *@dev --dev

### Generate the default conf
You can generate the default conf by running in the root directory of your project:

    python vendor/fansible/tywin/generate.py
    
You can now found your provisioning in the `devops` directory

### Provision the VM
You can create the VM with `vagrant up`.
Provision it with `vagrant provision`.

### Database configuration
Change the value of the database configuration in `devops/provisioning/hosts/group_vars/vagrant`

### Add some conf
Create the `.fansible.yml` file in the root diretory
Example:

    project_name: fansible-devops
    timezone: "Europe/Paris"
    port: 80
    hosts: all
    sudo: "true"
    
    vagrant:
      ip: 10.0.0.10
      box: "ubuntu/trusty64"
      memory: 1024
      cpus: 1
      exec: 100
      src: .


