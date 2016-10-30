import json
import time
from flask import session
from flask_socketio import emit, join_room, leave_room

from bot import medbot
from .. import socketio



@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    gender = session.get('gender')
    name = session.get('name')

    join_room(room)

    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    emit('status', {'msg': '<div class= "mdl-card__supporting-text">'
        + medbot.greet()+ name+'<br>'+ medbot.set_gender(gender)+' rigth?</div>\n'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    
    room = session.get('room')
    patient_msg = message['msg']
    

    bot_msg = medbot.speak(message['msg'])
    time.sleep(0.5)
    
    emit('status', {'msg': bot_msg +'</br>'}, room=room)

@socketio.on('geolocation', namespace='/chat')
def geolocation(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    medbot.user_location = (message['lat'], message['lng'])

@socketio.on('marker_select', namespace='/chat')
def marker_select(data):
    bot_msg = medbot.speak(msg=data['place_id'], state='SELECTED_CLINIC')
    room = session.get('room')
    emit('message', {'msg': '<span style="font-size:1em;">'
        + session.get('name')+ ': </span> ' 
        + bot_msg}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

