#!/usr/bin/env python
import os
import logging
import click
import yaml
from pathlib import Path
from iterfzf import iterfzf
import datetime

backup_limit = 10

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
    logging.debug(f"Checking if there's not more than {backup_limit} backup files in this directory")
    dirpath = os.path.dirname(os.path.abspath(filename))
    logging.debug(f"Getting all the files in {dirpath}")
    files = os.listdir(dirpath)
    logging.debug(f"These are all the files in the directory:\n{files}")
    logging.debug(f"Checking for all kcleaner backup files")
    files = [item for item in files if "kcleaner.bak" in item]
    logging.debug(f"These are the backup files in this folder:\n{files}")
    if len(files) > 10:
        logging.info(f"Cleaning up excess of backup files - we have {len(files)} already... - Removing the {len(files) - 10} oldest files")
        files.sort()
        for file in files[0:(len(files)-10)]:
            logging.debug(f"Removing File {file}")
            os.remove(f"{dirpath}/{file}")

def update_file(filename, yamldoc):
    test_file_exists(filename)
    if not test_file_exists(filename) and not "bak" in filename:
        logging.error("Cannot work with an empty file!, please check the path of your config file.")
    if "bak" in filename:
        check_and_cleanup_backups(filename)
    logging.debug(f"Opening write stream for file {filename}")
    with open(filename, 'w') as stream:
        try:
            logging.debug("Writing new yaml doc into the config file")
            yaml.dump(yamldoc, stream)
        except yaml.YAMLError as exc:
            logging.exception("Exception occured while trying to write Yaml file")

def get_file(filename):
    logging.debug(f'Trying to retrieve contents of file {filename}')
    if not test_file_exists(filename):
        logging.error("Cannot work with an empty file!, please check the path of your config file.")
        exit(10)
    with open(filename, 'r') as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.exception("Exception occured while trying to load Yaml file")
    logging.debug(f'File Contents\n{config_file}')
    logging.debug(f'Type of the file contents: {type(config_file)}')
    if config_file == None:
        logging.error("Config File is empty! Can't use it.")
        exit(11)
    elif type(config_file) == str:
        logging.error("Config File is not a valid yaml file!")
        exit(12)
    return config_file

def test_file_exists(filename):
    logging.debug(f"checking if file {filename} exists...")
    exists = os.path.isfile(filename)
    if exists:
        logging.debug("File exists!")
    else:
        logging.info('Config File Not found!')
        # Keep presets
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
        dates.append((datetime.datetime.strptime("_".join(file.split('_')[0:2]), '%Y-%m-%d_%H-%M-%S').strftime("%c")))
    logging.debug(dates)
    backup_to_use = iterfzf(dates)
    return get_file(f"{backup_path}/{backup_to_use}")


def remove_resource(config_file, removing_type):
    logging.debug(f"Started removal of {removing_type}")
    resources_name_list = []
    logging.debug('gathering list of objects for the this resource type')
    for resource in config_file[removing_type]:
        resources_name_list.append(resource['name'])

    resources_to_remove = []
    logging.debug('Prompting for selection')
    resources_to_remove = (iterfzf(resources_name_list, multi=True))
    logging.debug('List of resources selected: {resources_to_remove}')
    if resources_to_remove == None:
        logging.error("No resources to remove selected!")
        exit()

    logging.debug(f"{len(config_file[removing_type])} {removing_type} before the removal")

    #TODO: Implement cross resource finding
    #response = ask_yn("Remove Related Resources?")
    #print(f"Your response = {response}")

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
            'contexts'
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
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

    kubeconfig_dir = os.path.dirname(os.path.abspath(kubeconfig))
    kubeconfig_backup = f"{kubeconfig_dir}/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_kcleaner.bak"

    if undo:
        logging.info(f"Undo flag was set! checking for the backup file...")
        logging.info(f'Searching for backup config file {kubeconfig_backup}')
        config_file_after = get_backup(kubeconfig_dir)
    else:
        config_file_before = get_file(kubeconfig)
        update_file(kubeconfig_backup, config_file_before)
        logging.info(f'Using resource {resource}')
        logging.debug(f'Config file to use: {kubeconfig}')
        if name == None:
            logging.info(f'Name is empty, using fzf to search for the resource to remove')
        else:
            logging.info(f'Name of the resource requested to remove: {name}')
        config_file_after = remove_resource(config_file_before, resource)
        logging.info(f'Backing up config file at {kubeconfig_backup} before doing anything')
        

    logging.debug(f"New Config file content: \n{config_file_after}")
    update_file(kubeconfig, config_file_after)

if __name__ == '__main__':
    cli(obj={})
