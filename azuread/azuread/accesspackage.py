import logging
import json

from . import core

def query(query):
    url = "https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages?$filter=%s" % (query)
    return core.get_graph_data(url)

def get_by_displayname(name):
    return query("displayName eq '%s'" % (name))

def get():
    url = 'https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages'
    return core.get_graph_data(url)

def create(data):
    url = 'https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages'

    logging.debug(json.dumps(data, indent=4))
    return core.create_graph_data(url, data)

def update(id, data):
    url = 'https://graph.microsoft.com/v1.0/identityGovernance/entitlementManagement/accessPackages'

    logging.debug(json.dumps(data, indent=4))
    return core.update_graph_data(url + '/' + id, data)
