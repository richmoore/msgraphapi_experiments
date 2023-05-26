import logging

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
