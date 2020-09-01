from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, send, leave_room, emit
import requests
from requests.exceptions import ConnectionError
# b0qhpry9_6FoEBH1tGXEWrWkYZJgo3uSLuQv3uhwR - Project Key
# b0qhpry9 - Project ID
from deta import Deta
import os
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

endpoints = {"room": ["https://f82f2c67cbfc46aa8e43a89d705a0b0e.i.tgcloud.io:14240/gsqlserver/gsql/codecheck", "tigergraph", "Browser123"]}
link = "https://f82f2c67cbfc46aa8e43a89d705a0b0e.i.tgcloud.io:14240/gsqlserver/gsql/codecheck"
username = "tigergraph"
password = "Browser123"

@app.route('/')
def sessions():
    return render_template('index.html')


@socketio.on('join')
def join(data):
    room = data['room']
    room = str(room)
    box_link = data["link"]
    box_username = data["username"]
    box_password = data["password"]
    join_room(room)

    if room not in endpoints:
        endpoints[room] = [box_link, box_username, box_password]
    # else:
    #     if room not in endpoints:
    #         endpoints[room] = [data['link'], data['username'], data['password']]
    #         link = endpoints[room][0]
    #         username = endpoints[room][1]
    #         password = endpoints[room][2]
    #     else:
    #         link = endpoints[room][0]
    #         username = endpoints[room][1]
    #         password = endpoints[room][2]

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

@socketio.on("send message")
def message(data):


    # try:
    print(link, username, password)
    room = data['room']
    code = {
            "code": data['message'],
            "graph": "MyGraph"
            }
    box_link = endpoints[room][0]
    box_username = endpoints[room][1]
    box_password = endpoints[room][2]
    response = requests.post(box_link, 
                        json=code, auth=(box_username, box_password))
        
    emit('broadcast message', data['message'], room=room)
    emit('broadcast errors', response.json(), room=room)
    # except ConnectionError as e:
    #     emit('error', "Please try again with a valid box credentials, or check if your box is up", room=room)





if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))

    app.run(debug=True)
