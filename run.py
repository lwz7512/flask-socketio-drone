from flask import *
# from flask_socketio import *
from flask_socketio import SocketIO, send, emit

import takeoff
import mission
import land

# ================== Init the server ==============
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(app, logger=True)


# ================ app route =======================

# Send HTML!
@app.route('/')
def root():    
    return "Hello world!"

# Returns a random number
@app.route('/random')
def random():  
    from random import randint  
    html = str(randint(1, 100))
    return html

# Prints the user id
@app.route('/user/<id>')
def user_id(id):
    return str(id)

# Display the HTML Page & pass in a username parameter
@app.route('/html/<username>')
def html(username):
    return render_template('index.html', username=username)


# ============ socket event handler =================


@socketio.on('connect')
def test_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# Receive a message from the front end HTML
@socketio.on('send_message')   
def message_recieved(data):
    msg = data['text']
    print(">>>>>> got: "+ msg + " <<<<<<<<<<")
    emit('message_from_server', {'text':'Recieved message : '+msg} , broadcast=True)

@socketio.on('drone_takeoff')
def drone_takeoff(data):
    print('>>> to takeoff ...')
    emit('message_from_server', {'text':'Recieved message : takeoff'} , broadcast=True)
    takeoff.main()


@socketio.on('drone_mission')
def drone_mission(data):
    print('>>> to run mission ...')
    emit('message_from_server', {'text':'Recieved message : mission'} , broadcast=True)
    mission.main()


@socketio.on('drone_land')
def drone_land(data):
    print('>>> to landing ...')
    emit('message_from_server', {'text':'Recieved message : landing'} , broadcast=True)
    land.main()


# ================ main ================================

# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(app, host='0.0.0.0', port=8000, debug=False)