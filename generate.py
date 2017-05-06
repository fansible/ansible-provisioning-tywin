import os, shutil, sys, imp, json, socket

if sys.version_info.major != 2:
    print "This program only works with python 2.6 or 2.7 (like Ansible)"
    exit()

def module_exists(module_name, comment):
    try:
        imp.find_module(module_name)
    except ImportError:
        print "You have to install "+module_name
        print comment
        exit()

#We check if the python dependencies have been installed
module_exists('yaml',"Have a look at: http://stackoverflow.com/questions/14261614/how-do-i-install-the-yaml-package-for-python")
import yaml
module_exists('jinja2', "Have a look at: http://stackoverflow.com/questions/6726983/jinja-install-for-python")
from jinja2 import Environment, FileSystemLoader

#Directories
DIRECTORY_DEVOPS = 'devops'
DIRECTORY_PROVISIONING = DIRECTORY_DEVOPS+'/provisioning'
DIRECTORY_PROVISIONING_ROLES = DIRECTORY_PROVISIONING+'/roles'
DIRECTORY_PROVISIONING_VARS = DIRECTORY_PROVISIONING+'/vars'
DIRECTORY_PROVISIONING_HOSTS = DIRECTORY_PROVISIONING+'/hosts'
DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS = DIRECTORY_PROVISIONING+'/group_vars'
DIRECTORY_PROVISIONING_FANSIBLE_ROLES = DIRECTORY_PROVISIONING_ROLES+'/fansible-roles'
DIRECTORY_DEPLOYMENT = DIRECTORY_DEVOPS+'/deploy'
DIRECTORY_DEPLOYMENT_STAGES = DIRECTORY_DEPLOYMENT+'/stages'
DIRECTORY_TYWIN = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_TYWIN_ROLES = DIRECTORY_TYWIN+'/roles_files'
DIRECTORY_TYWIN_CONFIG = DIRECTORY_TYWIN+'/config'
DIRECTORY_TYWIN_TEMPLATES = DIRECTORY_TYWIN+'/templates'

#Files
FANSIBLE_YAML = '.fansible.yml'
DEFAULT_SYMFONY_YAML = DIRECTORY_TYWIN_CONFIG+'/default.symfony.yml'
DEFAULT_LARAVEL_YAML = DIRECTORY_TYWIN_CONFIG+'/default.laravel.yml'
DEFAULT_NODEJS_YAML = DIRECTORY_TYWIN_CONFIG+'/default.nodejs.yml'

#Configs
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(DIRECTORY_TYWIN_TEMPLATES),
    trim_blocks=True
)
VAGRANT_IP = '10.0.0.10'

def main(argv):
    project_config = project_type_finder()
    #Remove slashes from the project name
    project_config['project_name'] = project_config['project_name'].replace('/','-')
    #Ask the user what he needs
    user_input(project_config)
    add_vars_files(project_config)
    create_directories()
    copy_roles_files(project_config)
    #generate playbook, ansible.cfg, Vagrantfile, ..
    generate_basic_provisioning_files_if_they_dont_exist(project_config)
    if project_config['project_type'] == 'symfony':
        generate_deployment_files(project_config)

    print "\033[92mThe provisioning has been generated. Check out the `devops` directory\033[0m"

def user_input(project_config):
    project_name_input = raw_input("What's the name of the project? (Default:"+
            project_config['project_name']+ ")"
        )
    if project_name_input:
        #TODO: regexp to control that the name won't make any errors
        project_config['project_name'] = project_name_input

    optional_roles = ['ubuntu-mysql', 'ubuntu-postgresql', 'ubuntu-mongodb']
    for key, role in enumerate(optional_roles):
        if not(role in project_config['roles']):
            do_you_need_this_role(role, project_config)

    project_config['vagrant_ip'] = ask_vagrant_ip()        

def do_you_need_this_role(role_name, project_config):
    user_answer = raw_input("Do you need "+ role_name +"[y/N] ?")
    if user_answer == "y" or user_answer == "Y":
        project_config['roles'].append(role_name)

def ask_vagrant_ip():
    vagrant_ip_input = raw_input("What's the ip adress of the Vagrant machine? (Default:"+
        VAGRANT_IP + ")")
    if vagrant_ip_input:
        try:
            socket.inet_aton(vagrant_ip_input)
            #legal ip
            return vagrant_ip_input
        except socket.error:
            return ask_vagrant_ip()
    else:
        return VAGRANT_IP       

#TODO:add more project types
def project_type_finder():
    #Php projects
    if os.path.exists('composer.json'):
        composer_json = read_file_and_return_dict('composer.json')
        if 'require' in composer_json:
            if 'symfony/symfony' in composer_json['require']:
                return symfony_config_loader(composer_json)
            if 'laravel/framework' in composer_json['require']:
                return laravel_config_loader(composer_json)

    #NodeJs projects
    if os.path.exists('package.json'):
        return node_config_loader()

    return ask_project_type()

def ask_project_type():
    user_answer = raw_input("Is this a Symfony project (s), Laravel project (l) or a Node.js (n) project? [S/l/n] ?")
    if user_answer == "s" or user_answer == "S" or user_answer == "" or user_answer == "y":
        print 'Symfony project'
        return read_file_and_return_dict(DEFAULT_SYMFONY_YAML)

    if user_answer == "n" or user_answer == "N":
        print 'Node.js project'
        return read_file_and_return_dict(DEFAULT_NODEJS_YAML)

    if user_answer == "l" or user_answer == "L":
        print 'Laravel project'
        return read_file_and_return_dict(DEFAULT_LARAVEL_YAML)

    print 'You can only choose between "s", "l" or "n"'

    return ask_project_type()

def node_config_loader():
    print 'NodeJs project detected...'
    project_config = read_file_and_return_dict(DEFAULT_NODEJS_YAML)
    package_json = read_file_and_return_dict('package.json')
    if 'name' in package_json:
        project_config['project_name'] = package_json['name']
    if 'dependencies' in package_json:
        deps = package_json['dependencies']
        if 'mongodb' in deps or 'loopback-connector-mongodb' in deps:
            print "Database detected from package.json: mongodb"
            project_config['roles'].append('ubuntu-mongodb')
        if 'pg' in deps or 'loopback-connector-postgresql' in deps:
            print "Database detected from package.json: postgresql"
            project_config['roles'].append('ubuntu-postgresql')

    return project_config


def symfony_config_loader(composer_json):
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
                project_config['roles'].append('ubuntu-mysql')
            if parameters_yml['parameters']['database_driver'] == "pdo_pgsql":
                print "Database detected from parameters.yml: postgresql"
                project_config['roles'].append('ubuntu-postgresql')
            #TODO: add mongo
    else:
        print "No database detected from parameters.yml"

    return project_config

def laravel_config_loader(composer_json):
    print 'Laravel project detected...'
    project_config = read_file_and_return_dict(DEFAULT_LARAVEL_YAML)
    if 'name' in composer_json:
        project_config['project_name'] = composer_json['name']
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
        DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS,
        DIRECTORY_DEPLOYMENT,
        DIRECTORY_DEPLOYMENT_STAGES
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Build the tree of vars that will be used to generate template files
def add_vars_files(project_config):
    project_config["vars_files"] = []
    for key, role in enumerate(project_config['roles']):
        print "The role " + role + " has been added to the provisioning"
        # We build the list of vars files that will have to be copied
        if os.path.exists(DIRECTORY_TYWIN_TEMPLATES+'/ansible/vars/'+role+'.yml'):
            project_config["vars_files"].append(role)

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

def generate_file_if_it_doesnt_exist(target_file, source_file, project_config):
    if not os.path.exists(target_file):
        generate_template_file(source_file, project_config, target_file)

def copy_roles_files(project_config):
    for key, role in enumerate(project_config['roles']):
        if role in project_config['vars_files']:
            generate_template_file(
                '/ansible/vars/'+role+'.yml',
                project_config,
                DIRECTORY_PROVISIONING_VARS+'/'+role+'.yml'
            )

        #We override if the role already exists
        if os.path.exists(DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+role):
            shutil.rmtree(DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+role)
        shutil.copytree(
            DIRECTORY_TYWIN_ROLES+'/'+role,
            DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+role
        )

def read_file_and_return_dict(name):
    if os.path.exists(name):
        fv = open(name)
        if ".json" in name:
            returned_dict = json.load(fv)
        else:
            returned_dict = yaml.safe_load(fv)
        fv.close()
    else:
        returned_dict = {}

    return returned_dict

def generate_basic_provisioning_files_if_they_dont_exist(project_config):
    copy_if_doesnt_exist(DIRECTORY_TYWIN_TEMPLATES+'/ansible/ansible.cfg', 'ansible.cfg')

    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING+'/playbook.yml', 'ansible/playbook.yml', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_VARS+'/main.yml', 'ansible/vars/main.yml', project_config)
    generate_file_if_it_doesnt_exist('Vagrantfile', 'Vagrantfile', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS+'/vagrant', 'hosts/vagrant', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS+'/staging', 'hosts/staging', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS+'/prod', 'hosts/prod', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/vagrant', 'group_vars/vagrant', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/staging', 'group_vars/prod_staging', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/prod', 'group_vars/prod_staging', project_config)

def generate_deployment_files(project_config):
    copy_if_doesnt_exist(DIRECTORY_TYWIN_TEMPLATES+'/capistrano/Gemfile', 'Gemfile')
    copy_if_doesnt_exist(DIRECTORY_TYWIN_TEMPLATES+'/capistrano/Gemfile.lock', 'Gemfile.lock')
    copy_if_doesnt_exist(DIRECTORY_TYWIN_TEMPLATES+'/capistrano/Capfile', 'Capfile')
    generate_file_if_it_doesnt_exist(DIRECTORY_DEPLOYMENT+'/deploy.rb', 'capistrano/deploy/deploy.rb', project_config)
    generate_file_if_it_doesnt_exist(DIRECTORY_DEPLOYMENT_STAGES+'/prod.rb', 'capistrano/deploy/stages/prod.rb', project_config)

def copy_if_doesnt_exist(src, target):
    if not os.path.exists(target):
        shutil.copy(src, target)

if __name__ == "__main__":
    main(sys.argv[1:])
