import requests
import time
import threading
from colorama import Fore, Style
import os
import json
from send_message import send_message

base_url = "https://antiserious.us/"
api_url = base_url + "/api/v2/pleroma/chats"
auth_token = os.environ['AuthToken'] 

def send_message(chat_id, message):
    url = f"{base_url}/api/v1/pleroma/chats/{chat_id}/messages"
    headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
    data = {"content": message}
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        print(f"{Fore.GREEN}Sent message to chat ID {chat_id}: {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Failed to send message to chat ID {chat_id}: {response.status_code}{Style.RESET_ALL}")
        print("Response content:", response.text)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Read settings from settings.json
def read_settings():
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    return settings

# Update settings in settings.json
def update_settings(settings):
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4)

def get_user_id(username):
    url = f"{base_url}/api/v1/accounts/{username}"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        return data["id"]
    return None

def handle_rank_command(chat_id, message, author_name):
    command_parts = message.split()
    if len(command_parts) == 3 and command_parts[2] == "dev":
        settings = read_settings()
        developer_names = settings["developer_names"]
        if author_name in developer_names:
            user_id = get_user_id(command_parts[1])
            if user_id:
                # Update settings to add new developer
                developer_names.append(command_parts[1])
                settings["developer_names"] = developer_names
                settings["developer_promotion"] = True
                update_settings(settings)
                
                send_message(chat_id, f":key_win95: {command_parts[1]} has been promoted to developer.")
            else:
                send_message(chat_id, "User not found.")
        else:
            send_message(chat_id, ":card_reader_decline: You don't have permission to promote this user.")
    else:
        send_message(chat_id, "Invalid usage. Use !rank {username} dev")

def check_for_commands():
    while True:
        try:
            clear_console()
            response = requests.get(api_url, headers={"Authorization": f"Bearer {auth_token}"})
            if response.ok:
                data = response.json()
                for chat in data:
                    chat_id = chat["id"]
                    message = chat["last_message"]["content"]
                    author_names = chat["account"]["display_name"]
                    print(f"{Fore.LIGHTBLUE_EX}Got new messages from {author_names}!{Style.RESET_ALL}")
                    if message.startswith("!"):
                        command_name = message.split()[0][1:]
                        if command_name == "ping":
                            from commands.ping import handle_command
                            handle_command(chat_id, auth_token, base_url)
                        elif command_name == "help":
                            from commands.help import handle_command
                            handle_command(chat_id, auth_token, base_url, author_names)
                        elif command_name == "story":
                            from commands.story import handle_command
                            handle_command(chat_id, auth_token, base_url, author_names)
                        elif command_name == "media":
                            from commands.media import handle_command
                            handle_command(chat_id, auth_token, base_url, message)
                        elif command_name == "spin":
                            from commands.spin import handle_command
                            handle_command(chat_id, auth_token, base_url, author_names)

                        elif command_name == "rank":
                            handle_rank_command(chat_id, message, author_names)
                        else:
                            try:
                                command_module = __import__(f"commands.{command_name}", fromlist=[""])
                                command_module.handle_command(chat_id, auth_token, base_url, author_names, message)
                            except ImportError:
                                send_message(chat_id, f"Unknown command: {command_name}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        time.sleep(5)

if __name__ == "__main__":
    commands_thread = threading.Thread(target=check_for_commands)
    commands_thread.start()

    commands_thread.join()
