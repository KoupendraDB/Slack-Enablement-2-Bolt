import requests, json
from .endpoints import names as endpointNames

config = {}
with open('./config.json') as config_file:
	config = json.load(config_file)

server = config['backend_server_uri']

def make_request(name, data = {}, headers = {}, url_param = {}, params={}):
    headers['Accept'] = '*/*';
    headers['Content-Type'] = 'application/json'
    endpoint = endpointNames[name]['ENDPOINT']
    request_type = endpointNames[name]['METHOD']
    if len(url_param):
        endpoint = endpoint.format(**url_param)
    uri = server + endpoint
    print(request_type, uri)
    if request_type == 'GET':
        response = requests.get(uri, data=json.dumps(data), headers=headers, params=params)
    elif request_type == 'DELETE':
        response = requests.delete(uri, data=json.dumps(data), headers=headers)
    elif request_type == 'POST':
        response = requests.post(uri, data=json.dumps(data), headers=headers)
    elif request_type == 'PATCH':
        response = requests.patch(uri, data=json.dumps(data), headers=headers)
    print(response)
    return response.json() if response else {}