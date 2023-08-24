# This file contains the components needed to take photos with the meraki camera and post them to a webex space.

# Copyright (C) 2023 Procellis Technology, Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
