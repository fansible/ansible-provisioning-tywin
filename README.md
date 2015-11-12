# Fansible Tywin
Create easily your Ansible provisioning for Node.js and Symfony projects.

This project is still under development, all issues and questions are **very welcomed**.

It has already been used to create new projects that are currently in production =).

##Requirements
This have been tested with the Ubuntu OS. It should work with many other various Debian distribution. Feel free to share your advice for the other OS..
This is what you will need to install if you haven't done yet:

* **Python 2.7**
* [Ansible](http://docs.ansible.com/intro_installation.html) (1.8.4 or higher)
* [Vagrant](http://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
* nfs `sudo apt-get install nfs-kernel-server`
* PyYAML and Jinja2 for python

## How to use it

1) Installation

    git clone git@github.com:fansible/tywin.git ~/tywin --recursive

2) Generate the default conf

You can generate the default conf by running in the root directory of your project:

    python ~/tywin/generate.py

You can now find your provisioning in the `devops` directory

3) Create the VM
You can create the VM with `vagrant up`.

4) Put your ssh key in the vagrant 

i) Copy your public key `cat ~/.ssh/id_rsa.pub`

ii) Log in the vagrant with `vagrant ssh`

iii) Add your key in the authorized_keys file: `nano .ssh/authorized_keys`

iv) Exit the VM and try to log in with `ssh vagrant@10.0.0.10`

If it's OK you can provision the VM

5) Provision the VM

Provision it with `ansible-playbook -i devops/provisioning/hosts/vagrant devops/provisioning/playbook.yml`.

Your VM is now ready ! =)

### Database configuration
Change the value of the database configuration in `devops/provisioning/hosts/group_vars/vagrant`

### Go further: customize your provisioning
What you can do:

1) Add your roles in the `devops/provisioning/roles` directory.

2) Modify the playbook to call your roles.

3) Overide vars (in `devops/provisioning/vars`).

## Road map
Follow the next things that will be done and vote for your favorite feature on the [trello board](https://trello.com/b/IlQopRrK/fansible-tywin)

##Thanks
A lot of roles have been created by other people.
I mainly found them in three places where really nice roles are being maintained:
https://github.com/ANXS, https://github.com/Stouts and https://github.com/geerlingguy.

Thanks a lot to [pjan vandaele](https://twitter.com/pjan),
[Kirill Klenov](https://github.com/klen) and [Jeff Geerling](http://jeffgeerling.com/)
for the amazing job they have done.

Special thanks to my friend [Simon](http://sconstans.fr/).

Maxime
