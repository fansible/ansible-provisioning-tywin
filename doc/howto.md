# How to use it

1) Installation.

    git clone git@github.com:fansible/tywin.git ~/tywin

2) Generate the default conf

You can generate the default conf by running in the root directory of your project:

    python ~/tywin/generate.py

You can now find your provisioning in the `devops` directory

3) Create the VM
You can create the VM with `vagrant up`.

4) Assuming that your key is in `~/.ssh/id_rsa.pub`, put your ssh key in the vagrant to be able to ssh into it:


    vagrant ssh -c "echo '`cat ~/.ssh/id_rsa.pub`' >> ~/.ssh/authorized_keys"

If it's OK you can provision the VM

5) Provision the VM

Provision it with `ansible-playbook -i devops/provisioning/hosts/vagrant devops/provisioning/playbook.yml`.
If something goes wrong you can go inside you vagrant and try do execute manually in your shell the Ansible task that is failing.

After that, your VM is now ready! You can see your project in your browser at the IP's adress (10.0.0.10 if you haven't changed anything) =)

6) Now you can do the same for your staging/production environment.
Update the file in `devops/provisioning/hosts/staging` and add the IP or domain of your server.

### Database configuration
Change the value of the database configuration in `devops/provisioning/group_vars/vagrant`

### Go further: customize your provisioning
What you can do:

1) Add your roles in the `devops/provisioning/roles` directory.

2) Modify the playbook to call your roles.

3) Overide vars (in `devops/provisioning/vars`).

If you want to have more information on the use of Ansible/Vagrant for you development environment, I wrote a [blog post about it](http://cloudacademy.com/blog/deploy-web-applications-on-iaas-with-ansible/).
