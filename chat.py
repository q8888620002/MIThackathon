#!/bin/env python
from app import create_app, socketio
from diagnosis import clinics

app = create_app(debug=True)


if __name__ == '__main__':
    socketio.run(app)
    
