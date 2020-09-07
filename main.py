from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, send, leave_room, emit
import requests
from requests.exceptions import ConnectionError
import os
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

endpoints = {"room": ["https://hey.i.tgcloud.io:14240/gsqlserver/gsql/codecheck", "tigergraph", "Password"]} # Stores Box credentials for every room
link = "hey"
username = "tigergraph"
password = "Password"
graphname = "graphname"

@app.route('/')
def sessions():
    return render_template('index.html')

# Add the user to their specific room, and stores the box credentials in the dictionary
@socketio.on('join')
def join(data):
    room = data['room']
    room = str(room)
    box_link = data["link"]
    box_username = data["username"]
    box_password = data["password"]
    box_graphname = data["graphname"]
    join_room(room)

    if room not in endpoints:
        endpoints[room] = [box_link, box_username, box_password, box_graphname]
    emit('joinedroom', "joinedroom", room=room, broadcast=True, include_self=False)
    
# Removes the user from the room
@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

# Triggers everytime textarea changes, emits the updated textarea to everyone in the room and also emits the Errors/Warnings
@socketio.on("send message")
def message(data):



    print(link, username, password)
    room = data['room']
    code = {
            "code": data['message'],
            "graph": endpoints[room][3]
            }
    box_link = endpoints[room][0]
    box_username = endpoints[room][1]
    box_password = endpoints[room][2]
    # Making a request to the box specific codecheck endpoint
    response = requests.post(box_link, 
                        json=code, auth=(box_username, box_password))
        
    emit('broadcast message', data['message'],  room=room, broadcast=True, include_self=False)
    emit('broadcast errors', response.json(), room=room)






if __name__ == '__main__':
    app.run(debug=True)
