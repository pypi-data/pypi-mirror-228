import subprocess
import sys
import os
from rich.progress import Progress
from rich import print
import importlib.util


# Check if a module is installed
def is_module_installed(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None


# Function to install dependencies from requirements.txt
def install_dependencies():
    try:
        # Read the list of dependencies from requirements.txt
        with open("requirements.txt", "r") as requirements_file:
            dependencies = [line.strip() for line in requirements_file.readlines()]

        if not dependencies:
            print("[red]No dependencies found in requirements.txt[/red]")
            sys.exit(1)

        # Use pip to install the dependencies
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Installing Dependencies...", total=len(dependencies)
            )

            for dependency in dependencies:
                subprocess.run(["pip", "install", dependency])
                progress.update(task, completed=1)

        print("[green]Dependencies installed successfully[/green])")
    except Exception as e:
        print(f"[red]Error: {e}")
        sys.exit(1)


# Check if dependencies are already installed
required_modules = ["socketio", "rich"]
for module in required_modules:
    if not is_module_installed(module):
        print(f"[yellow]{module} is not installed. Installing now...[/yellow]")
        install_dependencies()

# Rest of code
import socketio
import threading
from threading import Thread
from datetime import datetime

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
    print("[red]A user with the same username already exists in this room.[/red]")
    os._exit(0)


@sio.on("connect")
def on_connect():
    print("[bold green]Connected to the server")
    request_secret_key()  # Request the secret key from the server


@sio.on("disconnect")
def on_disconnect():
    print("[red]Disconnected from the server[/red]")


@sio.on("authentication_failed")
def authentication_failed():
    print("[yellow]Authentication failed.[/yellow]")
    os._exit(0)


def request_secret_key():
    sio.emit("request_secret_key")


def send_message(message, username, room):
    timestamp = datetime.now().strftime("%H:%M:%S")
    sio.emit("message", {"message": message, "username": username, "room": room})


def leave_chat(username, room):
    sio.emit("leave", {"username": username, "room": room})
    sio.disconnect()
    print("[bold green]Leaving the chat and exiting...")
    raise SystemExit



EMOTICON_TO_EMOJI = {
    ":)": "😊",
    ":(": "😢",
    ";)": "😉",
    ":D": "😄",
    ":P": "😛",
    "<3": "❤️",
    ":|": "😐",
    ":O": "😮",
    ":/": "😕",
    ":3": "😺",
    ":*": "😘",
    ":')": "😂",
    ":|": "😐",
    ":'(": "😥",
    ":>": "😆",
    ":<": "😔",
    ":]": "😃",
    ":[": "😞",
    ":}": "😃",
    ":{": "😞",
    ":v": "😬",
    ":^)": "😆",
    ":3": "😺",
    "O:)": "😇",
    "xD": "😆",
    "XD": "😆",
    "<3": "❤️",
    "^_^": "😊",
    "-_-": "😑",
}


def handle_input(username, room):
    paste_mode = False
    paste_buffer = []
    stick_mode = False
    stick_file_path = ""

    while True:
        message = input(": ")

        # Convert emoticons to emojis if found
        for emoticon, emoji in EMOTICON_TO_EMOJI.items():
            message = message.replace(emoticon, emoji)

        if message.strip()=="/help":
            print(
                """
                [bold blue]Available Commands:[/bold blue]
                /help - Displays this message
                /paste - Activate paste mode
                /stick - Activate stick mode
                /send - Send the code in paste mode and stick mode
                /exit - Leave the chat
                """
            )

        elif message.strip() == "/exit":
            leave_chat(username, room)
        elif message.startswith("/paste"):
            paste_mode = True
            paste_buffer = []
            print(
                "[bold blue]Paste mode activated. Enter your code. Type '/send' to send and exit paste mode.[/bold blue]"
            )
        elif paste_mode:
            if message.strip() == "/send":
                if paste_buffer:
                    code_message = "\n".join(paste_buffer)
                    send_message(code_message, username, room)
                    print(
                        "[bold green]Code sent. Reverting to message mode."
                    )
                    paste_mode = False
                    paste_buffer = []
                else:
                    print(
                        "[yellow]No code to send. Reverting to message mode.[/yellow]"
                    )
                    paste_mode = False
            else:
                paste_buffer.append(message)
        elif message.startswith("/stick"):
            stick_mode = True
            print(
                "[yellow]Stick mode activated. Enter the path of the file to send. Type '/send' to send and exit stick mode.[/yellow]"
            )
        elif stick_mode:
            if message.strip() == "/send":
                if stick_file_path:
                    if os.path.exists(stick_file_path):
                        file_link = f'[{os.path.basename(stick_file_path)}]({stick_file_path.replace(" ", "%20")})'
                        send_message(file_link, username, room)
                        print(
                            "[bold green]File link sent. Reverting to message mode."
                        )
                    else:
                        print(
                            "[yellow]File not found. Reverting to message mode.[/yellow]"
                        )
                    stick_mode = False
                    stick_file_path = ""
                else:
                    print(
                        "[red]No file path provided. Reverting to message mode.[/red]"
                    )
                    stick_mode = False
            else:
                stick_file_path = message
        else:
            send_message(message, username, room)


if __name__ == "__main__":
    server_url = "http://34.125.3.30:3389"  # Replace with your server URL
    sio.connect(server_url)

    username = input("Enter your username: ")
    room = input("Enter the chatroom name: ")

    sio.emit("join", {"room": room, "username": username})

    print(f"Welcome to the '{room}' chatroom, {username}!\n")

    thread = threading.Thread(target=sio.wait)
    thread.daemon = True
    thread.start()

    try:
        handle_input(username, room)
    except KeyboardInterrupt:
        leave_chat(username, room)