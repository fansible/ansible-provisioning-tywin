# Fansible Tywin
Create easily your Ansible provisioning.
This project is still under development and **not stable yet**. 

##Requirements
This have been tested with the Ubuntu OS. It should work with many other various Debian distribution. Feel free to share your advice for the other OS..
This is what you will need to install if you haven't done yet:

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

4) Provision it
Provision it with `ansible-playbook -i devops/provisioning/hosts/vagrant devops/provisioning/playbook.yml`.

Your VM is now ready ! =)

### Database configuration
Change the value of the database configuration in `devops/provisioning/hosts/group_vars/vagrant`

### Customize your provisioning
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
