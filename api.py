from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import base64
from middleware import authorize_request
from slack import prepare_message, send_message
from PIL import Image

import random
import os

app = Flask(__name__)
app.before_request(authorize_request)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from PrintDatabase import PrintDatabase
db_manager = PrintDatabase(app)

key = os.environ.get('REQ_KEY')

## api
@app.route("/api/printer", methods=["POST"])
def api_printer():
    inp = request.get_json()
    print("recieved printer event:", inp["title"], inp["message"])

    if(inp["title"] == "started"):
        printId = db_manager.insert_print(inp["message"])

    printId = db_manager.insert_print_event(inp["message"], inp["title"], inp["attachments"][0]["base64"])

    message = prepare_message(inp, printId)
    print(message)

    send_message(message)

    return {200: "success"}

@app.route("/api/claim", methods=["POST"])
def api_claim():
    
    printId = request.args.get("printId")
    owner = request.json["owner"]
    db_manager.change_owner(printId, owner)

    return {200: "success"}

@app.route("/api/purge", methods=["POST"])
def api_purge(date):
    db_manager.purge_old_entries()

    return {200: "success"}

## frontend
@app.route("/")
def index():
    prints = db_manager.get_prints_with_latest_events(20)
    return render_template('index.html', prints=prints)

@app.route("/claim")
def claim():
    printO = db_manager.get_print_with_latest_event(request.args.get("printId"))
    if(printO=={}):
        return "Print not found", 404
    
    if(printO["owner"] != ""):        
        return "Print already claimed", 400

    return render_template('claim.html', print=printO)

@app.route("/image")
def image():
    printO = db_manager.get_print_with_latest_event(request.args.get("printId"))
    if(printO=={}):
        return "Print not found", 404
    
    image_binary = base64.b64decode(printO["picture"])
    img = Image.open(image_binary)
    flip_img = img.transpose(Image.FLIP_TOP_BOTTOM)

    response = Response(flip_img, mimetype='image/jpeg')
    
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
