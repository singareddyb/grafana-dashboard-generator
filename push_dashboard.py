from __future__ import print_function
from requests import Session
import os
import os.path
import sys
import json

class GrafanaAPIClient(object): 
    def __init__(self, bearer_token, grafana_api_base_url, folder_name):
        self.bearer_token = bearer_token
        self.grafana_api_base_url = grafana_api_base_url
        self.folder_name = folder_name
        self.session = Session()

    def __generate_headers(self):
        headers = dict()
        headers['Authorization'] = 'Bearer {0}'.format(self.bearer_token)
        headers['Content-Type'] = 'application/json'
         
        return headers

    def get_folder_id(self):
        method = 'GET'
        url_frag = 'folders'
        resp = self.session.request(method, '{0}/{1}'.format(self.grafana_api_base_url, url_frag), headers=self.__generate_headers())
 
        py_resp = json.loads(resp.content)
        for folder_obj in py_resp:
            if folder_obj['title'] == self.folder_name:
                return folder_obj['id']
                
        return None


    def create_dashboard(self, file):
        method = 'POST'
        url_frag = 'dashboards/db'
        new_file = file + '_folderId'
        with open(file, 'r') as fd:
            py_obj = json.load(fd)
            py_obj['folderId'] = self.get_folder_id()
            json_data = json.dumps(py_obj)
        with open(new_file, 'w') as fd:
            fd.write(json_data)
        
        with open(new_file, 'r') as fd:
            resp = self.session.request(method, '{0}/{1}'.format(self.grafana_api_base_url, url_frag), headers=self.__generate_headers(), data=fd.read())
        return resp.content

if __name__ == '__main__':
    parent = sys.argv[1]
    file = sys.argv[2]
    folder_name = sys.argv[3]
    api_token = sys.argv[4]
    base_url = sys.argv[5]
    
    client = GrafanaAPIClient(api_token, '{0}/api'.format(base_url), folder_name)

    print(client.create_dashboard(os.path.join(os.getcwd(), 'outputs/{0}/{1}'.format(parent, file))))
