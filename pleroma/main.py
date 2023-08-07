import requests
import time
import threading
from colorama import Fore, Style
import os
from send_message import send_message

base_url = "https://example.com/"
api_url = base_url + "/api/v2/pleroma/chats"
auth_token = "" # use https://tools.splat.soy/pleroma-access-token/

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

# This may be buggy, qwq
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
                    print(f"{Fore.LIGHTBLUE_EX}Got new messages from {author_names}! {uwu} {Style.RESET_ALL}")
                    if message.startswith("!"):
                        command_name = message.split()[0][1:]  # Get the command name without "!"
                        if command_name == "ping":
                            from commands.ping import handle_command
                            handle_command(chat_id, auth_token, base_url)
                        elif command_name == "help":
                            from commands.help import handle_command
                            handle_command(chat_id, auth_token, base_url)
                        elif command_name == "story":
                            from commands.story import handle_command
                            handle_command(chat_id, auth_token, base_url, author_names)
                        elif command_name == "media":  
                            from commands.media import handle_command
                            handle_command(chat_id, auth_token, base_url, message)  
                        elif command_name == "spin":  
                            from commands.spin import handle_command
                            handle_command(chat_id, auth_token, base_url, author_names )
    
                        else:
                            try:
                                command_module = __import__(f"commands.{command_name}", fromlist=[""])
                                command_module.handle_command(chat_id, auth_token, base_url, author_names)
                            except ImportError:
                                send_message(chat_id, f"Unknown command: {command_name}", auth_token, base_url)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        time.sleep(5) 

# Hey, mind giving this git repo a star? qwq
if __name__ == "__main__":
    commands_thread = threading.Thread(target=check_for_commands)
    commands_thread.start()

    commands_thread.join()
