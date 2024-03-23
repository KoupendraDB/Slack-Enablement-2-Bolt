import requests, json
from .endpoints import names as endpointNames

config = {}
with open('./config.json') as config_file:
	config = json.load(config_file)

server = config['backend_server_uri']

def make_request(name, request_type, data = {}, headers = {}):
    headers['Accept'] = '*/*';
    uri = server + endpointNames[name]
    if request_type == 'GET':
        response = requests.get(uri, headers=headers)
    elif request_type == 'DELETE':
        response = requests.delete(uri, headers=headers)
    elif request_type == 'POST':
        headers['Content-Type'] = 'application/json'
        response = requests.post(uri, data=json.dumps(data), headers=headers)
    elif request_type == 'PATCH':
        headers['Content-Type'] = 'application/json'
        response = requests.patch(uri, data=data, headers=headers)
    return response.json() if response else {}