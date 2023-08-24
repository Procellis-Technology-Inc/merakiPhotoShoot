# merakiPhotoShoot
Take pictures with Webex webhooks and your Meraki cameras.

## Technology stack: 
* Python 3.11+
* Flask
* Webex
* Meraki MV Cameras

## Use Case
This is a basic set of components for working with a Webex bot to use the Meraki MV APIs.  It is highly insecure, so it is not recommended in a private or live production environment.  The intention of this project was to share what we created with the hope that someone would take it and make something wonderful with it.

One use case we envisioned for this technology would be to check the occupancy of a garage with limited parking available.  Rather than opening the garage door to look inside, you could send a webex message and see how many available parking spaces there were.  It could also be used to check if the garbage and recycling had been taken out, whether lights were left on, who is ringing the doorbell, or whether a conference room was occupied.  In conjunction with a Meraki MT20 Open/Close sensor, it could be used to snap photos and share them on webex automatically when a server rack or door is opened.  It has been tested to work with Google Assistant to use voice commands to take the photo, though that implementation is beyond the scope of this repository.

## Security Issues
Webex bots can be added to any webex team without any sort of authorization check.  If the photos are being sent to the webex bot itself this means it could be used to take photos by a malicious agent.  To remediate this, photos should only be sent to a Webex Space in your organization.
When taking photos, privacy and data security could be compromised, so it is highly recommended to use this in a public area with the permission of those using the space.

## Installation Steps
1.	Install Python 3.11
2.	Clone the repository from https://github.com/Procellis-Technology-Inc/merakiPhotoShoot.git
3.	Create a virtual environment
```
Python -m venv venv
.\venv\Scripts\activate
```
4.	Install requirements
```
Pip install -r requirements.txt
```
5.	Rename config.yaml.sample to config.yaml

## Make a Webex Bot
https://developer.webex.com/my-apps/new/bot
1.	Enter a name
2.	Enter a username (must be unique)
3.	Enter a description of your bot
4.	Add bot to Webex using the plus button at the top of the webex app and entering the username you specified @webex.bot

## Configuration File (config.yaml)
1.	Navigate to developer.webex.com and log in
2.	Documentation > Access the API
3.	Copy your personal access token and paste it as api_key into the config.yaml file
4.	Choose any open port on your network and enter it as flask port (I use 12505)
5.	Make an API call to Webex using the following information
-	GET
-	https://webexapis.com/v1/rooms
-	Authorization: bearer {Api Key}
6.	Choose the room of your bot and copy the id to your config file
7.	Set bot name to whatever you want
8.	Set camera location to whatever you want
9.	Log into dashboard.meraki.com
10.	Cameras > monitor > cameras > select the camera you want > network
11.	Grab the serial number from the left pane and put in your config file
12.	Click on the person icon in the top right corner > my profile
13.	Scroll down to API access > generate a new API key > copy to sensor_key config file

## Running the application
In a terminal navigate to the root of your application and run
```
Python main.py
```

## Make a webhook
1.	Send the following API call
-	POST
-	https://webexapis.com/v1/webhooks
- Authorization Bearer {Api Key}
-  ###	Header
-  Content-Type: application/json
-  ###	Body
``` 
{
  "name": "<enter whatever you want>",
  "targetUrl": "http://<public URL where your script will run>:<port>",
  "resource": "messages",
  "event": "created",
  "filter": "roomId=<room id>"
}
```
## Testing
In Webex send a message to the bot’s room starting with “/say cheese”
If everything worked correctly, the bot should capture and display a still image from the camera you selected.
