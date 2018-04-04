import json
import requests
from requests.auth import HTTPBasicAuth


class OnosRest():

    def __init__(self):
        self.controller_ip = '192.168.139.130'
        self.api_url = 'http://%s:8181/onos/v1' % self.controller_ip
        self.credentials = ('onos', 'rocks')

    def get_devices(self):
        "Returns network devices file"

        url = self.api_url + '/devices'
        print(url)
        response = requests.get(url, auth=self.credentials)
        return response.json()

    def get_hosts(self):
        "Returns network devices file"

        url = self.api_url + '/hosts'
        print(url)
        response = requests.get(url, auth=self.credentials)
        return response.json()

    def get_network_config(self):
        "Returns network configuration file"    

        url = self.api_url + '/network/configuration'
        response = requests.get(url, auth=self.credentials)
        # return json.dumps(response.json(), indent=4, sort_keys=False)
        return response.json()

    def push_network_config(self, cfg_path):
        "Send network configuration to controller"

        url = self.api_url + '/network/configuration'
        config_file = json.dumps(self.load_json(cfg_path))

        response = requests.post(url, data=config_file, 
                                headers={"Content-Type": "application/json, Accept: application/json"})

    def load_json(self, path):
        "Loads json from file"
        with open(path) as f:
            return json.load(f)

    def get_device_id(self, devices):
        for device in devices['devices']:
            print(device['available'])

    def del_device(self, device_id):
        "Delete device with given id"
        url = self.api_url + '/devices/' + device_id
        response = requests.delete(url, auth=self.credentials)
        print(response)
        
    def delete_unavailable_devices(self):
        devices = self.get_devices()
        for device in devices['devices']:
            if device['available'] == False:
                print('Deleting device with id: ' + device['id'])
                self.del_device(device['id'])

    def get_all_flows(self):
        url = self.api_url + '/flows'
        response = requests.get(url, auth=self.credentials)
        return response.json()

    def del_all_flows(self):
        "Doesn't work - to be finnished"
        url = url = self.api_url + '/flows'
        flows = self.get_all_flows()
        response = requests.delete(url, data=flows, auth=self.credentials, headers={"Content-Type": "application/json"})
        print(response)

    






controller = OnosRest()
# print(json.dumps(controller.get_all_flows(), indent=4))
# print(json.dumps(controller.get_devices(), indent=4))


