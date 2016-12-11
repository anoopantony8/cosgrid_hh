import yaml, os
from os.path import join
f = open(join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml'))
resource_data = yaml.safe_load(f)

mail_id = resource_data['mail_id']
pwd = resource_data['password']
netjson_cloud_name = resource_data['netjson_cloud_name']
netjson_username = resource_data['netjson_username']
netjson_password = resource_data['netjson_password']
netjson_endpoint = resource_data['netjson_endpoint']

