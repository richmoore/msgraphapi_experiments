import logging
import argparse
import json
import yaml
import os

template_dir = 'templates'

def create_catalog(name, description, enabled=False):
    logging.debug('Building catalog %s', name)
    id = 'catalog-1'
    logging.debug('Created catalog with id %s', id)

    return id

def create_access_package(catalog_id, name, description, resources=[], hidden=False):
    logging.debug('Creating access package %s', name)
    id = 'package-1'

    for resource in resources:
        logging.debug('Adding resource %s', resource)

    logging.debug('Created access package %s', id)
    return id

def create_access_package_approval(package_id, config):
    logging.debug('Creating access package approval for %s', package_id)

    template_file = config['Template']

    with open(os.path.join(template_dir, template_file)) as f:
        approval = f.read()

        for approver in config['Approvers']:
            logging.debug('Adding approver %s', approver)

            # UPN or group
            if approver.find('@') != -1:
                logging.debug('Approver %s is user %s', approver, approver)
            else:
                logging.debug('Approver %s is group %s', approver, approver)

            
        print(approval)

def process_package(catalog_id, filename):
    logging.debug('Processing package file %s', filename)
    
    with open(filename) as f:
        config = yaml.safe_load(f)
 
    if not (('Name' in config) and ('Description' in config)
        and ('Groups' in config) and ('Template' in config)):
        raise Exception('Invalid package file', filename)

    package_id = create_access_package(catalog_id, config['Name'], config['Description'], config['Groups'])
    create_access_package_approval(package_id, config)
        

def process_directory(directory):
    logging.debug('Processing directory %s', directory)

    # Create the catalog
    catalog_file = os.path.join(directory, 'catalog.yaml')
    with open(catalog_file) as f:
        cat = yaml.safe_load(f)
        catalog_id = create_catalog(cat['Name'], cat['Description'])

    for entry in os.scandir(directory):
        if not entry.is_file():
            continue
        if entry.name == 'catalog.yaml':
            continue

        process_package(catalog_id, entry.path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('directory', help='Directory to process')

    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    if args.quiet:
        level = logging.WARN

    logging.basicConfig(level=level)

    process_directory(args.directory)