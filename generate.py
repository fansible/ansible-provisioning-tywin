import yaml, os, shutil, sys
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
                project_config['services'].append('mysql')
            if parameters_yml['parameters']['database_driver'] == "pdo_pgsql":
                print "Database detected from parameters.yml: postgresql"
                project_config['services'].append('postgresql')
            #TODO: add mongo
    else:
        print "No database detected from parameters.yml"

    return project_config

#TODO: make it pretty
#Create directories
def create_directories():
    if not os.path.exists(DIRECTORY_DEVOPS):
        os.makedirs(DIRECTORY_DEVOPS)
    if not os.path.exists(DIRECTORY_PROVISIONING):
        os.makedirs(DIRECTORY_PROVISIONING)
    if not os.path.exists(DIRECTORY_PROVISIONING_ROLES):
        os.makedirs(DIRECTORY_PROVISIONING_ROLES)
    if not os.path.exists(DIRECTORY_PROVISIONING_FANSIBLE_ROLES):
        os.makedirs(DIRECTORY_PROVISIONING_FANSIBLE_ROLES)
    if not os.path.exists(DIRECTORY_PROVISIONING_VARS):
        os.makedirs(DIRECTORY_PROVISIONING_VARS)
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS):
        os.makedirs(DIRECTORY_PROVISIONING_HOSTS)
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS):
        os.makedirs(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS)

# Build the tree of vars that will be used to generate template files
def build_config(project_config):
    #TODO: create a serie of question to generate a custom fansible yaml file
    config_fansible = read_file_and_return_dict(FANSIBLE_YAML)
    # Overide the default project config with the .fansible.yml config
    overide_dict(project_config, config_fansible)

    #TODO:change that for a more dynamic way (reading the roles directory)
    known_services = read_file_and_return_dict(KNOWN_SERVICES)

    project_config["selected_services"] = []
    project_config["vars_files"] = []

    project_config["known_services"] = known_services
    # Calculate selected known_services
    for key, service in enumerate(project_config['services']):
        if service in project_config["known_services"]:
            project_config['selected_services'].append(service)
            print "The service " + service + " has been added to the provisioning"
            service_name = project_config["known_services"][service]['role']
            # We build the list of vars files that will have to be copied
            if os.path.exists(DIRECTORY_TYWIN_TEMPLATES_ANSIBLE_VARS+'/'+service_name+'.yml'):
                project_config["vars_files"].append(service_name)
        else:
            print "Sorry the service "+service+" is unknow by Fansible/Tywin yet"

    return project_config

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

def copy_roles_files(project_config):
    for key, service in enumerate(project_config['selected_services']):
        service_name = project_config['known_services'][service]['role']

        if service_name in project_config['vars_files']:
            generate_template_file(
                '/Ansible/Vars/'+service_name+'.yml',
                project_config,
                DIRECTORY_PROVISIONING_VARS+'/'+service_name+'.yml'
            )

        #We override if the role already exists
        if os.path.exists(DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+service_name):
            shutil.rmtree(DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+service_name)
        shutil.copytree(
            DIRECTORY_TYWIN_ROLES+'/'+service_name,
            DIRECTORY_PROVISIONING_FANSIBLE_ROLES+'/'+service_name
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
    #generate playbooks if not exists
    if not os.path.exists(DIRECTORY_PROVISIONING+'/playbook.yml'):
        generate_template_file('Ansible/playbook.yml', project_config, DIRECTORY_PROVISIONING+'/playbook.yml')
    # We don't override main vars file
    if not os.path.exists(DIRECTORY_PROVISIONING_VARS+'/main.yml'):
        generate_template_file(
            '/Ansible/Vars/main.yml',
            project_config,
            DIRECTORY_PROVISIONING_VARS+'/main.yml'
        )
    #generate the vagrantfile if it doesn't exist
    if not os.path.exists('Vagrantfile'):
        generate_template_file('Vagrantfile', project_config, 'Vagrantfile')
    #TODO: refacto use a function
    #generate the vagrant inventory file if doesn't exist
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS+'/vagrant'):
        generate_template_file('hosts/vagrant', project_config, DIRECTORY_PROVISIONING_HOSTS+'/vagrant')
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS+'/staging'):
        generate_template_file('hosts/staging', project_config, DIRECTORY_PROVISIONING_HOSTS+'/staging')
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS+'/prod'):
        generate_template_file('hosts/prod', project_config, DIRECTORY_PROVISIONING_HOSTS+'/prod')
    #generate group_vars vars files if they don't exist
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/vagrant'):
        generate_template_file('group_vars/vagrant', project_config, DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/vagrant')
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/staging'):
        generate_template_file('group_vars/staging', project_config, DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/staging')
    if not os.path.exists(DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/prod'):
        generate_template_file('group_vars/prod', project_config, DIRECTORY_PROVISIONING_HOSTS_GROUP_VARS+'/prod')

#TODO: create verbose options
if __name__ == "__main__":
    main(sys.argv[1:])
