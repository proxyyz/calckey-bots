# commands/spin.py
import random
import os
import requests
from send_message import send_message 
# qwq 

def get_random_rarity():
    file_path = os.path.join(os.path.dirname(__file__), 'knives.txt')
    with open(file_path, 'r') as file:
        rarity_list = file.readlines()
    return random.choice(rarity_list).strip()

def handle_command(chat_id, auth_token, base_url, author_name):
    random_rarity = get_random_rarity()
    knife_rarity = random_rarity.capitalize()
    
    message = f"Congratulations {author_name}! You got a {knife_rarity} for the Butterfly Knife!"

    if random.random() < 0.1:  # chance for a trash skin, 1 = 10%, 2 = 20%. etc
        message = f"What the scallop, {author_name}. You got a less valuable skin."
    
    if random_rarity in ['Doppler', 'Ultraviolet', 'Lore', 'Crimson Red', 'Fade', 'Marble Fade']:
        message += f" Since it's rare, you get verified!"
        # Log to Discord webhook
        discord_webhook_url = ''
        log_data = {
            'content': f"{author_name} spun a {knife_rarity} for the Butterfly Knife!"
        }
        requests.post(discord_webhook_url, json=log_data)
    
    send_message(chat_id, message, auth_token, base_url)
