import os, shutil, sys, imp

def module_exists(module_name, helpfulLink):
    try:
        imp.find_module(module_name)
    except ImportError:
        print "You have to install "+module_name
        print "Have a look at: "+helpfulLink
        exit()

#We check if the python dependencies have been installed
module_exists('yaml',"http://stackoverflow.com/questions/14261614/how-do-i-install-the-yaml-package-for-python")
import yaml
module_exists('jinja2', "http://stackoverflow.com/questions/6726983/jinja-install-for-python")
from jinja2 import Environment, FileSystemLoader

#Directories
DIRECTORY_DEVOPS = 'devops'
DIRECTORY_PROVISIONING = DIRECTORY_DEVOPS+'/provisioning'
DIRECTORY_PROVISIONING_ROLES = DIRECTORY_PROVISIONING+'/roles'
DIRECTORY_PROVISIONING_VARS = DIRECTORY_PROVISIONING+'/vars'
DIRECTORY_PROVISIONING_HOSTS = DIRECTORY_PROVISIONING+'/hosts'
DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS = DIRECTORY_PROVISIONING+'/group_vars'
DIRECTORY_PROVISIONING_FANSIBLE_ROLES = DIRECTORY_PROVISIONING_ROLES+'/fansible-roles'
DIRECTORY_TYWIN = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_TYWIN_ROLES = DIRECTORY_TYWIN+'/roles'
DIRECTORY_TYWIN_CONFIG = DIRECTORY_TYWIN+'/config'
DIRECTORY_TYWIN_TEMPLATES = DIRECTORY_TYWIN+'/templates'
DIRECTORY_TYWIN_TEMPLATES_ANSIBLE = DIRECTORY_TYWIN_TEMPLATES+'/Ansible'
DIRECTORY_TYWIN_TEMPLATES_ANSIBLE_VARS = DIRECTORY_TYWIN_TEMPLATES_ANSIBLE+'/Vars'

#Files
FANSIBLE_YAML = '.fansible.yml'
DEFAULT_SYMFONY_YAML = DIRECTORY_TYWIN_CONFIG+'/default.symfony.yml'
DEFAULT_NODEJS_YAML = DIRECTORY_TYWIN_CONFIG+'/default.nodejs.yml'
KNOWN_SERVICES = DIRECTORY_TYWIN_CONFIG+'/known_services.yml'

#Configs
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(DIRECTORY_TYWIN_TEMPLATES),
    trim_blocks=True
)

def main(argv):
    project_config = project_type_finder()
    #Build config reading .fansible.yml file
    build_config(project_config)
    #Create all the needed directories
    create_directories()
    #Copy all the roles files
    copy_roles_files(project_config)
    #generate playbook, ansible.cfg, Vagrantfile, ..
    generate_basic_provisioning_files_if_they_dont_exist(project_config)

    print "The provisioning has been generated. Check out the `devops` directory"

#TODO:add more project types
def project_type_finder():
    #Php projects
    if os.path.exists('composer.json'):
        composer_json = read_file_and_return_dict('composer.json')
        if 'require' in composer_json:
            if 'symfony/symfony' in composer_json['require']:

                return symfony_config_loader(composer_json )
    #NodeJs projects
    if os.path.exists('package.json'):
        print 'NodeJs project detected...'
        project_config = read_file_and_return_dict(DEFAULT_NODEJS_YAML)
        package_json = read_file_and_return_dict('package.json')
        if 'name' in package_json:
            project_config['project_name'] = package_json['name']
        if 'dependencies' in package_json:
            deps = package_json['dependencies']
            if 'mongodb' in deps or 'loopback-connector-mongodb' in deps:
                print "Database detected from package.json: mongodb"
                project_config['services'].append('ubuntu-mongodb')
            if 'pg' in deps or 'loopback-connector-postgresql' in deps:
                print "Database detected from package.json: postgresql"
                project_config['services'].append('ubuntu-postgresql')

        return project_config

    print 'Project type unknown yet. This program only knows Symfony and Nodejs projects.'
    exit()

def symfony_config_loader(composer_json ):
    print 'Symfony project detected...'
    project_config = read_file_and_return_dict(DEFAULT_SYMFONY_YAML)
    if 'name' in composer_json:
        project_config['project_name'] = composer_json['name']
    parameters_yml = read_file_and_return_dict('app/config/parameters.yml')
    if 'parameters' in parameters_yml:
        if 'database_driver' in parameters_yml['parameters']:
            project_config['database_name'] = parameters_yml['parameters']['database_name']
            project_config['database_user'] = parameters_yml['parameters']['database_user']
            project_config['database_password'] = parameters_yml['parameters']['database_password']

            if parameters_yml['parameters']['database_driver'] == "pdo_mysql":
                print "Database detected from parameters.yml: mysql"
                project_config['services'].append('ubuntu-mysql')
            if parameters_yml['parameters']['database_driver'] == "pdo_pgsql":
                print "Database detected from parameters.yml: postgresql"
                project_config['services'].append('ubuntu-postgresql')
            #TODO: add mongo
    else:
        print "No database detected from parameters.yml"

    return project_config

#Create directories
def create_directories():
    directories = [
        DIRECTORY_DEVOPS,
        DIRECTORY_PROVISIONING,
        DIRECTORY_PROVISIONING_ROLES,
        DIRECTORY_PROVISIONING_FANSIBLE_ROLES,
        DIRECTORY_PROVISIONING_VARS,
        DIRECTORY_PROVISIONING_HOSTS,
        DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Build the tree of vars that will be used to generate template files
def build_config(project_config):
    #TODO?: create a serie of question to generate a custom fansible yaml file, yeoman?
    config_fansible = read_file_and_return_dict(FANSIBLE_YAML)
    # Overide the default project config with the .fansible.yml config
    overide_dict(project_config, config_fansible)

    project_config["known_services"] = os.listdir(DIRECTORY_TYWIN_ROLES)
    project_config["selected_services"] = []
    project_config["vars_files"] = []

    # Calculate selected known_services
    for key, service in enumerate(project_config['services']):
        if service in project_config["known_services"]:
            project_config['selected_services'].append(service)
            print "The service " + service + " has been added to the provisioning"
            # We build the list of vars files that will have to be copied
            if os.path.exists(DIRECTORY_TYWIN_TEMPLATES_ANSIBLE_VARS+'/'+service+'.yml'):
                project_config["vars_files"].append(service)
        else:
            print "Sorry the service "+service+" is unknow by Fansible/Tywin yet"

    return project_config

# Overide values in a base dict with values from another dict
def overide_dict(base, new):
    if hasattr(new, 'items'):
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

def copy_roles_files(project_config):
    for key, service in enumerate(project_config['selected_services']):
        if service in project_config['vars_files']:
            generate_template_file(
                '/Ansible/Vars/'+service+'.yml',
                project_config,
                DIRECTORY_PROVISIONING_VARS+'/'+service+'.yml'
            )

        #We override if the role already exists
        if os.path.exists(DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+service):
            shutil.rmtree(DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+service)
        shutil.copytree(
            DIRECTORY_TYWIN_ROLES+'/'+service,
            DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+service
        )

def read_file_and_return_dict(name):
    if os.path.exists(name):
        fv = open(name)
        returned_dict = yaml.safe_load(fv)
        fv.close()
    else:
        returned_dict = {}

    return returned_dict

def generate_basic_provisioning_files_if_they_dont_exist(project_config):
    #Copy ansible.cfg
    if not os.path.exists('ansible.cfg'):
        shutil.copy(DIRECTORY_TYWIN_TEMPLATES+'/Ansible/ansible.cfg', 'ansible.cfg')

    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING+'/playbook.yml', 'Ansible/playbook.yml', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_VARS+'/main.yml', 'Ansible/Vars/main.yml', project_config)
    generate_file_if_it_doesnt_exist('Vagrantfile', 'Vagrantfile', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS+'/vagrant', 'hosts/vagrant', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS+'/staging', 'hosts/staging', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS+'/prod', 'hosts/prod', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/vagrant', 'group_vars/vagrant', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/staging', 'group_vars/prod_staging', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/prod', 'group_vars/prod_staging', project_config)

def generate_file_if_it_doesnt_exist(target_file, source_file, project_config):
    if not os.path.exists(target_file):
        generate_template_file(source_file, project_config, target_file)

#TODO: create verbose options, check out yeoman
if __name__ == "__main__":
    main(sys.argv[1:])
