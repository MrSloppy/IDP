from flask import Flask, render_template, request
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
async_mode = None
if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        socketio.emit('emergency', {'data': request.form.to_dict()})
    return render_template('startpage.html')

if __name__ == '__main__':
    port = 5000
    debug = True
    socketio.run(app, debug=debug, host='0.0.0.0', port=port)