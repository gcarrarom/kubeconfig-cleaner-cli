#!/usr/bin/env python
import os
import logging
import click
import yaml
from pathlib import Path
from iterfzf import iterfzf

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

def update_file(filename, yamldoc):
    test_file_exists(filename)
    if not test_file_exists(filename) and not "bak" in filename:
        logging.error("Cannot work with an empty file!, please check the path of your config file.")
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

    kubeconfig_backup = f"{kubeconfig}.bak"

    if undo:
        logging.info(f"Undo flag was set! checking for the backup file...")
        logging.info(f'Searching for backup config file {kubeconfig_backup}')
        config_file_after = get_file(kubeconfig_backup)
    else:
        config_file_before = get_file(kubeconfig)
        logging.info(f'Using resource {resource}')
        logging.debug(f'Config file to use: {kubeconfig}')
        if name == None:
            logging.info(f'Name is empty, using fzf to search for the resource to remove')
        else:
            logging.info(f'Name of the resource requested to remove: {name}')
        config_file_after = remove_resource(config_file_before, resource)
        logging.info(f'Backing up config file at {kubeconfig_backup} before doing anything')
        update_file(kubeconfig_backup, config_file_before)
        

    logging.debug(f"New Config file content: \n{config_file_after}")
    update_file(kubeconfig, config_file_after)

if __name__ == '__main__':
    cli(obj={})
