#!/usr/bin/env python3.7
import os
import logging
import click
import yaml
from pathlib import Path
from iterfzf import iterfzf


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    with open(filename, 'w') as stream:
        try:
            yaml.dump(yamldoc, stream)
        except yaml.YAMLError as exc:
            print(exc)

def get_file(filename):
    test_file_exists(filename)
    with open(filename, 'r') as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config_file

def test_file_exists(filename):
    logging.debug("checking if file {filename} exists...")
    exists = os.path.isfile(filename)
    if exists:
        logging.debug("File exists!")
    else:
        print('Config File Not found!')
        # Keep presets
        exit(10)

def remove_resource(config_file, removing_type):
    resources_name_list = []
    for resource in config_file[removing_type]:
        resources_name_list.append(resource['name'])

    resources_to_remove = []
    resources_to_remove = (iterfzf(resources_name_list, multi=True))
    if resources_to_remove == None:
        print("No resources to remove selected!")
        exit()

    print(resources_to_remove)
    print(f"{len(config_file[removing_type])} {removing_type} in the end")

    response = ask_yn("Remove Related Resources?")
    print(f"Your response = {response}")

    try:
        config_file[removing_type] = [item for item in config_file[removing_type] if item['name'] not in resources_to_remove]
    except KeyError:
        print(f"Something went wrong!!")

    print(f"{len(config_file[removing_type])} {removing_type} in the end")

    return config_file


@click.command()
@click.option('--module', '-m', type=click.Choice(['user', 'cluster', 'context']), default='cluster')
@click.option('--kubeconfig', '-k', default=f'{Path.home()}/.kube/config')
@click.option(
    '--name', '-n',
    help='Name of the entry to remove',
)
def main(module, name, kubeconfig):
    """
    A little CLI tool to help keeping our Config Files clean :)
    """

    config_file = get_file(kubeconfig)

    if module == 'cluster':
        removing_type = 'clusters'
    elif module == 'user':
        removing_type = 'users'
    elif module == 'context':
        removing_type = 'contexts'

    config_file = remove_resource(config_file, removing_type)
    

    update_file("./config", kubeconfig)