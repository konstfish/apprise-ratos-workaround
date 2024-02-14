import requests

import os

webhook_url = os.environ['SLACK_WEBHOOK_URL']
base_url = os.environ['BASE_URL']

key = os.environ.get('REQ_KEY')

def prepare_message(data, printId):
    image_url = f"{base_url}/image?key={key}&printId={printId}"

    if(data["title"] == "started"):
        claim_url = f"{base_url}/claim?key={key}&printId={printId}"
        message = f"Print {data['message']} started. Please <{claim_url}|claim your print> {image_url}"
        return message
    message = f"Print {data['message']} event: {data['title']} {image_url}"
    return message

def send_message(message):
    req = requests.post(webhook_url, json={"message": message})
    print("slack res: ", req.status_code)