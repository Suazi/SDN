import json
import requests
from requests.auth import HTTPBasicAuth


controller_ip = '192.168.139.130'
api_url = 'http://%s:8181/onos/v1' % controller_ip


def network_config(cfg_path):
    url = api_url + '/network/configuration'
    config_file = json.dumps(load_file(cfg_path))

    response = requests.post(url, data=config_file, headers={"Content-Type": "application/json, Accept: application/json"})




def load_file(path):
    with open(path) as f:
        return json.load(f)





def get_config():
    url = api_url + '/network/configuration'
    print url
    response = requests.get(url, auth=('onos', 'rocks'))
    print json.dumps(response.json(), indent=4, sort_keys=False)

get_config()


