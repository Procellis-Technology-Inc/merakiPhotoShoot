from flask import Flask, request, json
import requests, yaml
from messenger import Messenger
from camera import cameraSnapshot, howManyPeople

app = Flask(__name__)
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    port = config['APP']['flask_port']
    room_id = config['APP']['room_id']
    api_key = config['APP']['api_key']
    botName = config['APP']['bot_name']
    cameraLocation = config['APP']['camera_location']
msg = Messenger()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Receive a notification from Webex Teams or Meraki and take an action"""
    if request.method == 'GET':
        return f'Request received on local port {port}'
    elif request.method == 'POST':
        print(request.get_json())
        try:
            # Take a picture command
            if request.get_json()['intent']['name'] == "TakeAPicture":
                snapshot = cameraSnapshot()
                payload = json.dumps({"roomId": room_id, "text": "Cheese", "files": snapshot['url']})
                header = {'Authorization': f'Bearer {api_key}', "Content-Type": "application/json"}
                requests.post('https://webexapis.com/v1/messages', data=payload, headers=header)
            # How many people command
            elif request.get_json()['intent']['name'] == "HowManyPeople":
                howMany = howManyPeople()
                if howMany == 1:
                    msg.reply = f'There is {howMany} person in the {cameraLocation}.'
                else:
                    msg.reply = f'There are {howMany} people in the {cameraLocation}.'
                payload = json.dumps({"roomId": room_id, "text": msg.reply})
                header = {'Authorization': f'Bearer {api_key}', "Content-Type": "application/json"}
                requests.post('https://webexapis.com/v1/messages', data=payload, headers=header)
        except KeyError:
            try:
                if 'application/json' in request.headers.get('Content-Type'):
                    data = request.get_json()
                    if msg.bot_id == data.get('data').get('personId'):
                        return 'Just talking to myself'
                    else:
                        msg.room_id = data.get('data').get('roomId')

                        message_id = data.get('data').get('id')
                        msg.get_message(message_id)
                        if msg.message_text.startswith('/help') or msg.message_text.startswith('PlannerBot /help'):
                                msg.reply = "I know the following commands:\n"+"-"*25+f"\n/help - display this message\n/say cheese - I will take a picture of {cameraLocation} and post it here\n/how many - I will tell you how many people I detect in {cameraLocation}"
                                msg.post_message(msg.room_id, msg.reply)
                        elif msg.message_text.startswith('/say cheese') or msg.message_text.startswith(f'{botName} /say cheese'):
                            snapshot = cameraSnapshot()
                            payload = json.dumps({"roomId": room_id, "text": "Cheese", "files": snapshot['url']})
                            header = {'Authorization': f'Bearer {api_key}', "Content-Type": "application/json"}
                            requests.post('https://webexapis.com/v1/messages', data=payload, headers=header)
                        elif msg.message_text.startswith('/how many') or msg.message_text.startswith(f'{botName} /how many'):
                            howMany = howManyPeople()
                            if howMany == 1:
                                msg.reply = f'There is {howMany} person in the garage.'
                            else:
                                msg.reply = f'There are {howMany} people in the garage.'
                            msg.post_message(msg.room_id, msg.reply)
                        else:
                            msg.reply = f'Bot received message "{msg.message_text}." Please be aware this will not trigger any actions.  Type @ followed by {botName} /help for instructions.'
                            msg.post_message(msg.room_id, msg.reply)

                        return data
            except AttributeError:
                # print(request.get_json())
                return ("oops", 666)
        except AttributeError:
            # print(request.get_json())
            return ("oops", 666)
        else:
            return ('Wrong data format', 400)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=port, ssl_context=('adhoc'), debug=True)
    app.run(host="0.0.0.0", port=port, debug=True)