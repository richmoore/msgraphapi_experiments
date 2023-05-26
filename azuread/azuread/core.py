import requests
import logging
import json

from . import internal

def get_graph_data(url, pagination=True):
    access_token = internal.get_access_token()
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
    access_token = internal.get_access_token()
    headers = {'Authorization': 'Bearer ' + access_token}

    graph_result = requests.post(url=url, headers=headers, json=data)

    if graph_result.status_code != 201:
        logging.error('Creation failed')
        logging.debug(graph_result.json())
        raise IOError("Unable to create object")

    return graph_result.json()

def update_graph_data(url, data):
    access_token = internal.get_access_token()
    headers = {'Authorization': 'Bearer ' + access_token}

    graph_result = requests.patch(url=url, headers=headers, json=data)

    if graph_result.status_code != 204:
        logging.error('Update failed')
        logging.debug(graph_result.json())
        raise IOError("Unable to update object")

    return
