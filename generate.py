import yaml, os, shutil, sys
from jinja2 import Environment, FileSystemLoader

DIRECTORY_DEVOPS = 'devops'
DIRECTORY_PROVISIONING = DIRECTORY_DEVOPS+'/provisioning'
DIRECTORY_PROVISIONING_ROLES = DIRECTORY_PROVISIONING+'/roles'
DIRECTORY_PROVISIONING_VARS = DIRECTORY_PROVISIONING+'/vars'
DIRECTORY_PROVISIONING_HOSTS = DIRECTORY_PROVISIONING+'/hosts'
DIRECTORY_PROVISIONING_FANSIBLE_ROLES = DIRECTORY_PROVISIONING_ROLES+'/fansible-roles'
DIRECTORY_TYWIN = 'vendor/fansible/tywin'
DIRECTORY_TYWIN_ROLES = DIRECTORY_TYWIN+'/roles'
DIRECTORY_TYWIN_TEMPLATES = DIRECTORY_TYWIN+'/templates'

TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(DIRECTORY_TYWIN_TEMPLATES),
    trim_blocks=True
)

def main(argv):
    project_type_finder()
    context = build_context()
    create_directories()
    copy_vars_files(context)

    #Copy roles if not exists
    if not os.path.exists(DIRECTORY_PROVISIONING_FANSIBLE_ROLES):
        shutil.copytree(DIRECTORY_TYWIN_ROLES, DIRECTORY_PROVISIONING_FANSIBLE_ROLES)
    #Copy ansible.cfg
    if not os.path.exists('ansible.cfg'):
        shutil.copy(DIRECTORY_TYWIN_TEMPLATES+'/Ansible/ansible.cfg', 'ansible.cfg')
    #generate playbooks if not exists
    if not os.path.exists(DIRECTORY_PROVISIONING+'/playbook.yml'):
        generate_template_file('Ansible/playbook.yml', context, DIRECTORY_PROVISIONING+'/playbook.yml')
    #generate vagrantfile if not exists
    if not os.path.exists('Vagrantfile'):
        generate_template_file('Vagrant/Vagrantfile', context, 'Vagrantfile')
    #generate vagrant inventory if not exists
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS+'/vagrant'):
        generate_template_file('Vagrant/vagrant', context, DIRECTORY_PROVISIONING_HOSTS+'/vagrant')
    #generate vagrant group_vars if not exists
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS+'/group_vars/vagrant'):
        generate_template_file('Vagrant/group_vars', context, DIRECTORY_PROVISIONING_HOSTS+'/group_vars/vagrant')

    print "Provisioning generated"

#TODO:add more project types
def project_type_finder():
    if os.path.exists('composer.json'):
        if 'symfony/symfony' in open('composer.json').read():
            print 'Symfony project detected...'
    else:
        print 'Project type unknown...'

#TODO: make it pretty
#Create directories
def create_directories():
    if not os.path.exists(DIRECTORY_DEVOPS):
        os.makedirs(DIRECTORY_DEVOPS)
    if not os.path.exists(DIRECTORY_PROVISIONING):
        os.makedirs(DIRECTORY_PROVISIONING)
    if not os.path.exists(DIRECTORY_PROVISIONING_ROLES):
        os.makedirs(DIRECTORY_PROVISIONING_ROLES)
    if not os.path.exists(DIRECTORY_PROVISIONING_VARS):
        os.makedirs(DIRECTORY_PROVISIONING_VARS)
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS):
        os.makedirs(DIRECTORY_PROVISIONING_HOSTS)
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS+'/group_vars'):
        os.makedirs(DIRECTORY_PROVISIONING_HOSTS+'/group_vars')

# Build the tree of vars that will be used to generate template files
def build_context():
    # Get the project config
    f = open('.fansible.yml')
    config_fansible = yaml.safe_load(f)
    f.close()

    # Get the default config
    fv = open(DIRECTORY_TYWIN+'/default.fansible.yml')
    config_default = yaml.safe_load(fv)
    fv.close()

    # Overide the default config with the project config
    overide_dict(config_default, config_fansible)

    config_default["selected_services"] = []
    # Calculate selected known_services
    for key, service in enumerate(config_default['services']):
        if service in config_default['known_services']:
            config_default['selected_services'].append(service)
        else:
            print "Sorry the service "+service+" is unknow by Fansible/Tywin yet"

    return config_default

# Overide values in a base dict with values from another dict
def overide_dict(base, new):
    for k, v in new.items():
        if type(v) == dict:
            overide_dict(base[k],v)
        else:
            base[k] = v

# Render the template with a specific context
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

# Create the file with the template rendering
def generate_template_file(template_filename, context, dest):
    with open(dest, "w") as ft:
        file_rendered = render_template(template_filename, context)
        ft.write(file_rendered)

#TODO: render only the file that are not empty
def copy_vars_files(context):
    for key, service in enumerate(context['selected_services']):
        generate_template_file(
            '/Ansible/Vars/'+service+'.yml',
            context,
            DIRECTORY_PROVISIONING_VARS+'/'+service+'.yml'
        )

#TODO: create verbose options
if __name__ == "__main__":
    main(sys.argv[1:])
