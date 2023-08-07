# commands/ping.py
import os
import speedtest
import threading
from send_message import send_message

def get_internet_speed(chat_id, auth_token, base_url): # this is probably buggy af
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    internet_speed_response = f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps"
    send_message(chat_id, internet_speed_response, auth_token, base_url)

def get_cpu_usage(chat_id, auth_token, base_url):
    cpu_percent = os.popen("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\\1/'").read().strip()
    cpu_usage_response = f"CPU Usage: {cpu_percent}%"
    send_message(chat_id, cpu_usage_response, auth_token, base_url)

def get_storage_usage(chat_id, auth_token, base_url):
    total, used, free = os.popen("df -h / | tail -1 | awk '{print $2, $3, $4}'").read().split()
    storage_usage_response = f"Storage Usage: {used} used / {total} total"
    send_message(chat_id, storage_usage_response, auth_token, base_url)

def handle_command(chat_id, auth_token, base_url):
    wait_message = "Please wait 30-60 seconds while I gather the information."
    send_message(chat_id, wait_message, auth_token, base_url)

    # Start three threads to fetch internet speed, CPU usage, and storage usage simultaneously
    threading.Thread(target=get_internet_speed, args=(chat_id, auth_token, base_url)).start()
    threading.Thread(target=get_cpu_usage, args=(chat_id, auth_token, base_url)).start()
    threading.Thread(target=get_storage_usage, args=(chat_id, auth_token, base_url)).start()
