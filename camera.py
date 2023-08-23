import requests, yaml

with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    meraki_api_key = config['SENSOR']['sensor_key']
    #network_id = config['SENSOR']['sensor_network']
    cameraSerial = config['SENSOR']['camera_serial']

headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"X-Cisco-Meraki-API-Key": meraki_api_key}

params = None

def cameraSnapshot():
    try:
        msg = requests.post(f"https://api.meraki.com/api/v1/devices/{cameraSerial}/camera/generateSnapshot", headers=headers, params=params)
        if msg.ok:
            data = msg.json()
            return data
    except Exception as e:
        print("API Connection error: {}".format(e))

def howManyPeople():
    try:
        msg = requests.get(f"https://api.meraki.com/api/v1/devices/{cameraSerial}/camera/analytics/live", headers=headers, params=params)
        if msg.ok:
            data = msg.json()
            return data['zones']['0']['person']
    except Exception as e:
        print("API Connection error: {}".format(e))

#url = cameraSnapshot()
url = howManyPeople()
if url == 1:
    url = f'There is {url} person in the garage.'
else:
    url = f'There are {url} people in the garage.'
print(url)
