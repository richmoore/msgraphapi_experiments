import msal
import logging
import argparse
import json

import azuread

config = {
    'client_id': '06151c90-18e8-4d97-8acb-b27f64345df4',
    'client_secret': 'gd.8Q~64ai53WrxC4iWUE0G4zm_Cg4XIljJtsajT',
    'authority':  'https://login.microsoftonline.com/6070b75d-b1fd-4b18-88c5-ce973c637e3a',
    'scope': ['https://graph.microsoft.com/.default'] 
}


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')

    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    if args.quiet:
        level = logging.WARN

    logging.basicConfig(level=level)

    # Create an MSAL instance providing the client_id, authority and client_credential parameters
    client = msal.ConfidentialClientApplication(config['client_id'], authority=config['authority'], client_credential=config['client_secret'])
    azuread.set_msal_client(client, config['scope'])


#    results = azuread.get_access_packages()
#    print(json.dumps(results, indent=4))

    new_ap = {
        "displayName": "Python Created Package s",
        "description": "This is a test access package created from python",
        "isHidden": False,
        "catalog": {
            "id": "17834343-4a83-4d92-a72d-f6dd34445427"
        }
    }

    results = azuread.accesspackage.create(new_ap)
    print(json.dumps(results, indent=4))

    results = azuread.accesspackage.get()
    print(json.dumps(results, indent=4))

    for ap in results:
        if ap['displayName'] == 'Python Created Package':
            id = ap['id']
            del ap['id']

            ap['displayName'] = 'Python Updated Package 2'

            azuread.accesspackage.update(id, ap)
            break

    results = azuread.accesspackage.get()
    print(json.dumps(results, indent=4))

    results = azuread.accesspackage.get_by_displayname('Python Updated Package')
    print(json.dumps(results, indent=4))
