# commands/help.py
from main import read_settings
def handle_command(chat_id, auth_token, base_url, author_name):
    from send_message import send_message
    
    settings = read_settings()  # Read settings from settings.json
    developer_names = settings["developer_names"]
    
    if author_name in developer_names:
        send_message(chat_id, ":key_win95: You're a developer!\n:tools: Commands: !ping, !story, !spin, !rank\n v.0.0.3 ALPHA_DEV", auth_token, base_url)
    else:
        send_message(chat_id, ":tools: Commands: !ping, !story, !spin\n v.0.0.3 ALPHA_PUBLIC", auth_token, base_url)
