# merakiPhotoShoot
Take pictures with webhooks and your Meraki cameras

## Installation Steps
1.	Install Python 3.11
2.	Clone the repository from https://github.com/Procellis-Technology-Inc/merakiPhotoShoot.git
3.	Create a virtual environment
- Python -m venv venv
- .\venv\Scripts\activate
4.	Install requirements
- Pip install -r requirements.txt
5.	Rename config.yaml.sample to config.yaml

## Make a Webex Bot
https://developer.webex.com/my-apps/new/bot
1.	Enter a name
2.	Enter a username (must be unique)
3.	Enter a description of your bot
4.	Add bot to Webex using the plus button at the top of the webex app and entering the username you specified @webex.bot

## Configuration File (config.yaml)
1.	Navigate to developer.webex.com
2.	Documentation > Access the API
3.	Copy your personal access token and paste it as api_key
4.	Choose any open port on your network and enter it as flask port (I use 12505)
5.	Make an API call to Webex using the following information
-	GET
-	https://webexapis.com/v1/rooms
-	Authorization: bearer <Api Key>
6.	Choose the room of your bot and copy the id to your config file
7.	Set bot name to whatever you want
8.	Set camera location to whatever you want
9.	Log into dashboard.meraki.com
10.	Cameras > monitor > cameras > select the camera you want > network
11.	Grab the serial number from the left pane and put in your config file
12.	Click on the person icon in the top right corner > my profile
13.	Scroll down to API access > generate a new API key > copy to config file

## Running the application
In a terminal navigate to the root of your application and run
- Python main.py

## Make a webhook
1.	Send the following API call
-	POST
-	https://webexapis.com/v1/webhooks
- Authorization Bearer <Api Key>
-  ###	Header
-  Content-Type: application/json
-  ###	Body
``` 
1. {
2.	  "name": "<enter whatever you want>",
3.	  "targetUrl": "<public URL where your script will run>:<port>”,
4.	  "resource": "messages",
5.	  "event": "created",
6.	  "filter": "roomId=<room id>"
7.	}
```
## Testing
In Webex send a message to the bot’s room starting with “/say cheese”
If everything worked correctly, the bot should capture and display a still image from the camera you selected.
