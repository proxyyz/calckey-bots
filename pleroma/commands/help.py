# commands/help.py

def handle_command(chat_id, auth_token, base_url):
    from send_message import send_message
    send_message(chat_id, "Commands: !ping, !story, !spin\n v.0.0.2 alpha", auth_token, base_url)
