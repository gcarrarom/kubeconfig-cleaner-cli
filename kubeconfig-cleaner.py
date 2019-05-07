#!/usr/bin/env python3.7
import click
import requests
import yaml
from pathlib import Path
from iterfzf import iterfzf



def update_file(filename, yamldoc):
    with open(filename, 'w') as stream:
        try:
            yaml.dump(yamldoc, stream)
        except yaml.YAMLError as exc:
            print(exc)

def get_file(filename):
    with open(filename, 'r') as stream:
        try:
            test = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return test

@click.command()
@click.argument(
    'module'
)
@click.option(
    '--name', '-n',
    help='Name of the entry to remove',
)
def main(module, name):
    """
    A little CLI tool to help keeping our Config Files clean :)
    """
    test = get_file("./config")

    if module == 'cluster':
        clusterList = []
        for cluster in test['clusters']:
            clusterList.append(cluster['name'])

        clustersToRemove = []
        clustersToRemove = (iterfzf(clusterList, multi=True))

        print(clustersToRemove)
        print(f"{len(test['clusters'])} Clusters in the end")

        try:
            test['clusters'] = [item for item in test['clusters'] if item['name'] not in clustersToRemove]
        except KeyError:
            print(f"Clusters not found!")

        print(f"{len(test['clusters'])} Clusters in the end")

        update_file("./config", test)



if __name__ == "__main__":
    main()