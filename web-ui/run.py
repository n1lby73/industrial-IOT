from webApp import app, socketio

app.app_context().push()

if __name__ == '__main__':
    socketio.run(app)
    # socketio.run(app, host='0.0.0.0', debug=True)