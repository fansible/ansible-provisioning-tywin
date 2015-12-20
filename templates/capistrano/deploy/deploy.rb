# config valid only for current version of Capistrano
lock '3.4.0'

set :deploy_to, "/var/www/{{ project_name }}"
#set :repo_url, 'git@github.com:fansible/tywin.git'
set :repo_url, 'git@github.com:CHANGEME/CHANGEME.git'

set :stages, %w(prod)

#TODO: change to var/logs,var/cache,bin/console ... if it's a SF3 project
set :log_path, "app/logs"
set :cache_path, "app/cache"
set :symfony_console_path, 'app/console'
set :linked_files, fetch(:linked_files, []).push('app/config/parameters.yml')
set :linked_dirs, [fetch(:log_path), "app/sessions", "web/uploads"]

set :ssh_user, 'www-data'
set :ssh_options, {
  forward_agent: true,
}

set :branch, 'master'
set :keep_releases, 3

set :composer_install_flags, '--prefer-dist --no-interaction --optimize-autoloader'
