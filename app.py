from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Configure logging with a more readable format
logging.basicConfig(
    filename='honeypot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_event(event_type, ip_address, message):
    logging.info(f"{event_type} - {ip_address} - {message}")

# Function to monitor the log file
def log_monitor():
    with open('honeypot.log', 'r') as f:
        f.seek(0, 2)  # Move to the end of the file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly
                continue
            
            # Parse the log line
            parts = line.strip().split(' - ')
            if len(parts) == 3:
                timestamp = parts[0]
                event_type = parts[1]
                message = parts[2]
                ip_address = "Unknown"  # You can modify this based on your log structure

                # Emit the log update
                socketio.emit('log_update', {
                    'timestamp': timestamp,
                    'event_type': event_type,
                    'ip_address': ip_address,
                    'message': message
                })

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(log_monitor)

if __name__ == '__main__':
    socketio.run(app, debug=True)