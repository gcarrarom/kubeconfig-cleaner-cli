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
    logging.debug("Opening write stream for file {filename}")
    with open(filename, 'w') as stream:
        try:
            logging.debug("Dumping new yaml doc into the config file")
            yaml.dump(yamldoc, stream)
        except yaml.YAMLError as exc:
            print(exc)

def get_file(filename):
    logging.debug(f'Trying to retrieve contents of file {filename}')
    test_file_exists(filename)
    with open(filename, 'r') as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    logging.debug(f'File Contents\n{config_file}')
    logging.debug(f'Type of the file contents: {type(config_file)}')
    if config_file == None:
        print("Config File is empty! Can't use it.")
        exit(11)
    elif type(config_file) == str:
        print("Config File is not a valid yaml file!")
        exit(12)
    return config_file

def test_file_exists(filename):
    logging.debug(f"checking if file {filename} exists...")
    exists = os.path.isfile(filename)
    if exists:
        logging.debug("File exists!")
    else:
        print('Config File Not found!')
        # Keep presets
        exit(10)

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
        print("No resources to remove selected!")
        exit()

    logging.debug(f"{len(config_file[removing_type])} {removing_type} before the removal")

    #TODO: Implement cross resource finding
    #response = ask_yn("Remove Related Resources?")
    #print(f"Your response = {response}")

    try:
        logging.debug('Removing resources...')
        config_file[removing_type] = [item for item in config_file[removing_type] if item['name'] not in resources_to_remove]
    except KeyError:
        print(f"Something went wrong!!")

    logging.debug(f"{len(config_file[removing_type])} {removing_type} in the end")

    return config_file


@click.group()
@click.option('--kubeconfig', '-k', default=f'{Path.home()}/.kube/config', help="Path to the config file to clean")
@click.pass_context
def cli(ctx, kubeconfig):
    """
    A little CLI tool to help keeping Config Files clean.
    """
    ctx.ensure_object(dict)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug(f'Config file to use: {kubeconfig}')
    ctx.obj['KUBE_CONFIG']=kubeconfig

@cli.command('contexts')
@click.option('--name', '-n', help='Name of the context to remove')
@click.pass_context
def contexts(ctx, name):
    config_file = get_file(ctx.obj['KUBE_CONFIG'])
    config_file = remove_resource(config_file, "contexts")

    update_file(ctx.obj['KUBE_CONFIG'], config_file)

@cli.command('clusters')
@click.option('--name', '-n', help='Name of the cluster to remove')
@click.pass_context
def clusters(ctx, name):
    resource = "clusters"
    config_file = get_file(ctx.obj['KUBE_CONFIG'])
    config_file = remove_resource(config_file, resource)

    update_file(ctx.obj['KUBE_CONFIG'], config_file)

@cli.command('users')
@click.option('--name', '-n', help='Name of the user to remove')
@click.pass_context
def users(ctx, name):
    resource = "users"
    config_file = get_file(ctx.obj['KUBE_CONFIG'])
    config_file = remove_resource(config_file, resource)

    update_file(ctx.obj['KUBE_CONFIG'], config_file)

if __name__ == '__main__':
    cli(obj={})