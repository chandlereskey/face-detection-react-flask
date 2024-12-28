import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Define event handlers
@sio.event
def connect():
    print('Connection established')

@sio.event
def connect_error(data):
    print('Connection failed')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('data')
def on_data(data):
    print('Data received:', data)

# Connect to the server
sio.connect('http://localhost:5001')

# Send a message to the server
sio.emit('data', {'message': 'Hello from Python client!'})

# Wait for events
sio.wait()
