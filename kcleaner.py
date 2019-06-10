#!/usr/bin/env python
import os
import logging
import click
import yaml
from pathlib import Path
from iterfzf import iterfzf
import datetime

backup_limit = 10
backup_date_format = '%Y-%m-%d_%H-%M-%S'

def ask_yn(yn_question, default='n'):
    tries = 0
    while True:
        response = input(f"{yn_question}(y/n)")
        tries = tries + 1
        if response in  ['y', 'n']:
            break
        elif tries > 2:
            response = default
            break
    return response

def check_and_cleanup_backups(filename):
    if filename == None:
        logging.error("Filename cannot be 'None'!")
        exit(40)
    logging.debug(f"Checking if there's not more than {backup_limit} backup files in this directory")
    dirpath = os.path.dirname(os.path.abspath(filename))
    logging.debug(f"Getting all the files in {dirpath}")
    files = os.listdir(dirpath)
    logging.debug(f"These are all the files in the directory:\n{files}")
    logging.debug(f"Checking for all kcleaner backup files")
    files = [item for item in files if "kcleaner.bak" in item]
    logging.debug(f"These are the backup files in this folder:\n{files}")
    if len(files) > backup_limit:
        logging.info(f"Cleaning up excess of backup files - we have {len(files)} already... - Removing the {len(files) - backup_limit} oldest files")
        files.sort()
        for file in files[0:(len(files)-backup_limit)]:
            logging.debug(f"Removing File {file}")
            os.remove(f"{dirpath}/{file}")
    else:
        logging.debug(f'We are bellow the backup limit, nothing to do here.')

def update_file(filename, yamldoc):
    file_exists(filename)
    if not file_exists(filename) and not "bak" in filename:
        logging.error("Cannot work with an empty file!, please check the path of your config file.")
    if "bak" in filename:
        check_and_cleanup_backups(filename)
    if yamldoc == None:
        logging.error("Yaml Value cannot be 'None'!")
        exit(30)
    elif yamldoc == "":
        logging.error("Yaml Value cannot be empty!")
        exit(31)
    logging.debug(f'Checking the type of the yamldoc: {type(yamldoc)}')
    if type(yamldoc) is not dict:
        try:
            yaml.safe_load(yamldoc)
        except:
            logging.exception("Yaml value is not valid!")
            exit(32)
    else:
        logging.debug(f"This is a dict yaml doc object. Should be fine to convert as yaml. Content:\n{yamldoc}")
    logging.debug(f"Opening write stream for file {filename}")
    with open(filename, 'w') as stream:
        try:
            logging.debug("Writing new yaml doc into the config file")
            yaml.dump(yamldoc, stream)
        except yaml.YAMLError as exc:
            logging.exception(f"Exception occured while trying to write Yaml file: {exc}")

def get_file(filename):
    logging.debug(f'Trying to retrieve contents of file {filename}')
    if not file_exists(filename):
        logging.error("Cannot work with an empty file!, please check the path of your config file.")
        exit(10)
    with open(filename, 'r') as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.exception(f"Exception occured while trying to load Yaml file: {exc}")
            exit(13)
    logging.debug(f'File Contents\n{config_file}')
    logging.debug(f'Type of the file contents: {type(config_file)}')
    if config_file == None:
        logging.error("Config File is empty! Can't use it.")
        exit(11)
    elif type(config_file) == str:
        logging.error("Config File is not a valid yaml file!")
        exit(12)
    return config_file

def file_exists(filename):
    logging.debug(f"checking if file {filename} exists...")
    if filename == None:
        logging.error("Filename cannot be 'None'")
        exit(20)
    elif filename == "":
        logging.error("Filename cannot be empty!")
        exit(21)
    exists = os.path.isfile(filename)
    if exists:
        logging.debug("File exists!")
    else:
        logging.info('Config File Not found!')
    return exists

def get_backup(backup_path):
    logging.debug(f"Checking all backups available in the directory {backup_path}")
    files = os.listdir(backup_path)
    logging.debug(f"These are all the files in the directory:\n{files}")
    logging.debug(f"Checking for all kcleaner backup files")
    files = [item for item in files if "kcleaner.bak" in item]
    logging.debug(f"These are the backup files in this folder:\n{files}")
    files.sort(reverse=True)
    dates = []
    for file in files:
        dates.append((datetime.datetime.strptime("_".join(file.split('_')[0:2]), backup_date_format).strftime("%c")))
    logging.debug(dates)
    backup_to_use = iterfzf(dates)
    logging.debug(f'Backup chosen: {backup_to_use}')
    backup_file_to_use = f"{datetime.datetime.strptime(backup_to_use, '%c').strftime(backup_date_format)}_kcleaner.bak"
    logging.debug(f'Backup file: {backup_file_to_use}')
    return get_file(f"{backup_path}/{backup_file_to_use}")


def remove_resource(config_file, removing_type):
    if config_file == None:
        logging.error(f'Config File cannot be "None"!')
        exit(50)
    if removing_type == None:
        logging.error(f'Removing type cannot be "None"!')
        exit(50)

    if removing_type == "" or config_file == "":
        logging.error(f'Parameters cannot be empty!')
        exit(51)

    if removing_type == 'token':
        removing_type = 'users'
        removing_token = True
    else: 
        removing_token = False
    logging.debug(f"Started removal of {removing_type}")
    resources_name_list = []
    logging.debug('gathering list of objects for the this resource type')
    if removing_token:
        for resource in config_file[removing_type]:
            try:
                logging.debug(f"{resource['user']['auth-provider']['config']['access-token']}")
                resources_name_list.append(resource['name'])
            except:
                continue
    else:
        for resource in config_file[removing_type]:
            resources_name_list.append(resource['name'])

    resources_to_remove = []
    logging.debug('Prompting for selection')
    resources_to_remove = (iterfzf(resources_name_list, multi=True))
    logging.debug('List of resources selected: {resources_to_remove}')
    if resources_to_remove == None or resources_to_remove == "":
        logging.error("No resources to remove selected!")
        exit(52)

    logging.debug(f"{len(config_file[removing_type])} {removing_type} before the removal")

    #TODO: Implement cross resource finding
    #response = ask_yn("Remove Related Resources?")
    #print(f"Your response = {response}")

    if removing_token:
        logging.debug(f"Removing token information from the user(s) {resources_to_remove}")
        for item in config_file[removing_type]:
            if item['name'] in resources_to_remove:
                logging.debug(f"removing tokens from user {item['name']}")
                item['user']['auth-provider']['config'].pop('access-token', None)
                item['user']['auth-provider']['config'].pop('expires-in', None)
                item['user']['auth-provider']['config'].pop('expires-on', None)
                item['user']['auth-provider']['config'].pop('refresh-token', None)
                logging.debug(f'Token Removed successfully!')

    else:
        try:
            logging.debug('Removing resources...')
            config_file[removing_type] = [item for item in config_file[removing_type] if item['name'] not in resources_to_remove]
        except KeyError:
            logging.exception(f"Something went wrong!!")

    logging.debug(f"{len(config_file[removing_type])} {removing_type} in the end")

    return config_file

@click.command()
@click.argument(
    "resource", 
    type=click.Choice(
        [
            'users', 
            'clusters', 
            'contexts',
            'token'
        ]
    ), 
    default='contexts'
)
@click.option(
    '--kubeconfig', '-k', default=f'{Path.home()}/.kube/config',
    help="path to the config file to clean"
)
@click.option(
    '--name', '-n',
    help='Name of the entry to remove',
)
@click.option(
    '--undo', '-u',
    help='Use this to roll back latest changes',
    is_flag=True
)
@click.option(
    '--debug', '-d',
    help='Use this to see debug level messages',
    is_flag=True
)
def cli(resource, name, kubeconfig, undo, debug):
    """
    A little CLI tool to help keeping Config Files clean :)
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug('Running with Debug flag')
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

    kubeconfig_dir = os.path.dirname(os.path.abspath(kubeconfig))
    kubeconfig_backup = f"{kubeconfig_dir}/{datetime.datetime.now().strftime(backup_date_format)}_kcleaner.bak"

    if undo:
        logging.info(f"Undo flag was set! checking for the backup file...")
        logging.debug(f'Searching for backup config file {kubeconfig_backup}')
        config_file_after = get_backup(kubeconfig_dir)
    else:
        config_file_before = get_file(kubeconfig)
        logging.debug(f'Backing up config file at {kubeconfig_backup} before doing anything')
        update_file(kubeconfig_backup, config_file_before)
        logging.info(f'Using resource {resource}')
        logging.debug(f'Config file to use: {kubeconfig}')
        if name == None:
            logging.debug(f'Name is empty, using fzf to search for the resource to remove')
        else:
            logging.debug(f'Name of the resource requested to remove: {name}')
        config_file_after = remove_resource(config_file_before, resource)
        
    logging.debug(f"New Config file content: \n{config_file_after}")
    update_file(kubeconfig, config_file_after)

if __name__ == '__main__':
    cli(obj={})
