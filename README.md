# Fansible Tywin
Create easily your Ansible provisioning

##Requirements
This have been tested with the Ubuntu OS. It should work with many other various Linux distribution. Feel free to share your advice for the other OS..
You will need to install if you haven't done yet:

* [Ansible](http://docs.ansible.com/intro_installation.html)
* [Composer](https://getcomposer.org/download/)
* [Vagrant](http://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
* nfs `sudo apt-get install nfs-kernel-server`

## How to use it

1) Installation

    composer require fansible/tywin *@dev --dev

2) Generate the default conf
You can generate the default conf by running in the root directory of your project:

    python vendor/fansible/tywin/generate.py
    
You can now found your provisioning in the `devops` directory

3) Provision the VM
You can create the VM with `vagrant up`.

Provision it with `vagrant provision`.

Your VM is now ready ! =)

### Database configuration
Change the value of the database configuration in `devops/provisioning/hosts/group_vars/vagrant`

### Add some conf
Create a `.fansible.yml` file in the root directory before you generate anything. 

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

### Customize your provisioning
What you can do:

1) Add your roles in the `devops/provisioning/roles` directory. 

2) Modify the playbook to call your roles.

3) Overide vars (in `devops/provisioning/vars`).




