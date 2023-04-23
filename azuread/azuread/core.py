import requests
import logging
import json

client = None
scope = None

def set_msal_client(msal_client, msal_scope):
    global client, scope
    client = msal_client
    scope = msal_scope

def get_access_token():
    # Firstly, try to lookup an access token in cache
    token_result = client.acquire_token_silent(scope, account=None)

    if token_result:
        logging.debug('Access token was loaded from cache.')
    else:
        token_result = client.acquire_token_for_client(scopes=scope)
        logging.debug('New access token aquired from AAD')

    if not 'access_token' in token_result:
        logging.error(token_result.get('error'))
        logging.error(token_result.get('error_description'))
        logging.error(token_result.get('correlation'))

        raise IOError('Unable to call graph API')
    
    return token_result['access_token']

def get_graph_data(url, pagination=True):
    access_token = get_access_token()
    headers = {'Authorization': 'Bearer ' + access_token}
    graph_results = []

    while url:
        try:
            graph_result = requests.get(url=url, headers=headers).json()
            graph_results.extend(graph_result['value'])
        
            if pagination:
                url = graph_result['@odata.nextLink']
            else:
                url = None
        except:
            break

    return graph_results

def create_graph_data(url, data):
    access_token = get_access_token()
    headers = {'Authorization': 'Bearer ' + access_token}

    graph_result = requests.post(url=url, headers=headers, json=data)

    if graph_result.status_code != 201:
        logging.error('Creation failed')
        logging.debug(graph_result.json())
        raise IOError("Unable to create object")

    return graph_result.json()

def update_graph_data(url, data):
    access_token = get_access_token()
    headers = {'Authorization': 'Bearer ' + access_token}

    graph_result = requests.patch(url=url, headers=headers, json=data)

    if graph_result.status_code != 204:
        logging.error('Update failed')
        logging.debug(graph_result.json())
        raise IOError("Unable to update object")

    return
