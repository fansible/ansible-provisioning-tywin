# Fansible Tywin: manage your symfony provisioning

## Still WIP
This is still under development: it is not a reliable repository yet

## How to use it

Coming soon: installation with composer

### Add some conf
Create the `.fansible.yml` file in the root diretory
Example:

    project_name: fansible-devops

    vagrant:
      ip: 10.0.0.10

### Generate
Run the script: `python vendor/fansible/tywin/generate.py`
You can now found your provisioning in the devops directory

### Provision the VM
You can create the VM with `vagrant up`.
Provision it with `vagrant provision`.
