import socketio
from threading import Thread
from datetime import datetime
import sys
import os

sio = socketio.Client()

def display_message(data, username):
    timestamp = datetime.now().strftime("%H:%M:%S")
    sender_username = data["username"]
    message = data["message"]
    
    if sender_username != username:
        print(f"{timestamp} - {sender_username}: {message}")
    else:
        print(f"{timestamp} - You: {message}")

@sio.on("message")
def handle_message(data):
    display_message(data, username)

@sio.on("username_exists")
def handle_username_exists():
    print("A user with the same username already exists in this room.")
    os._exit(0)

@sio.on("connect")
def on_connect():
    print("Connected to the server")

@sio.on("disconnect")
def on_disconnect():
    print("Disconnected from the server")

def send_message(message, username, room):
    timestamp = datetime.now().strftime("%H:%M:%S")
    sio.emit("message", {"message": message, "username": username, "room": room})

def leave_chat(username, room):
    sio.emit("leave", {"username": username, "room": room})
    sys.exit(0)

def handle_input(username, room):
    while True:
        message = input(": ")
        if message.strip() == "/exit":
            leave_chat(username, room)
        elif message.startswith("/paste"):
            send_message(message[7:], username, room)
        else:
            send_message(message, username, room)

if __name__ == "__main__":
    server_url = "http://34.125.3.30:3389"
    sio.connect(server_url)


    username = input("Enter your username: ")
    room = input("Enter the chatroom name: ")

    sio.emit("join", {"room": room, "username": username})

    print(f"Welcome to the '{room}' chatroom, {username}!\n")

    thread = Thread(target=sio.wait)
    thread.daemon = True
    thread.start()

    handle_input(username, room)
