from flask import Flask, render_template, request  # Tambahkan request di sini
from flask_socketio import SocketIO, send, emit
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Dictionary untuk menyimpan ID chat tiap klien
clients = {}

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Handle koneksi baru dari klien
@socketio.on('connect')
def handle_connect():
    chat_id = randint(1000, 9999)  # Buat ID acak untuk klien
    clients[request.sid] = chat_id  # Simpan chat ID berdasarkan session ID
    emit('chat_id', chat_id)  # Kirim chat ID ke klien

# Handle pesan yang diterima dari klien
@socketio.on('message')
def handle_message(msg):
    chat_id = clients[request.sid]  # Dapatkan chat ID klien yang mengirim
    message_with_id = f"Chat {chat_id}: {msg}"
    
    print(f"Pesan dari {chat_id}: {msg}")
    
    # Kirim pesan ke semua klien dengan chat ID
    send(message_with_id, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
