from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, send, leave_room, emit
import requests
# b0qhpry9_6FoEBH1tGXEWrWkYZJgo3uSLuQv3uhwR - Project Key
# b0qhpry9 - Project ID
from deta import Deta
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')


@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    room = str(room)
   

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

@socketio.on("send message")
def message(data):
    room = data['room']
    code = {
    "code": data['message'],
    "graph": "MyGraph"
    }
    response = requests.post("CODCHECK_ENDPOINT", 
                        json=code, auth=('USERNAME', 'PASSWORD'))
    emit('broadcast message', data['message'], room=room)
    emit('broadcast errors', response.json(), room=room)




if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))

    socketio.run(app, debug=True,  port=5000)
