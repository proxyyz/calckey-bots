import requests
import time

#  endpoints q_q
cat_api_url = 'https://api.thecatapi.com/v1/images/search?limit=1'
calckey_upload_url = 'https://domain.here/api/drive/files/upload-from-url'
calckey_notes_url = 'https://domain.here/api/notes/create'
drive_files_url = 'https://domain.here/api/drive/files'

# api keys qwq
cat_api_key = '' # get from thecatapi.com
calckey_api_key = '' # open your API console on calckey, make and get the token

def fetch_cat_image_url():
    headers = {'x-api-key': cat_api_key}
    response = requests.get(cat_api_url, headers=headers)
    cats_data = response.json()
    image_url = cats_data[0]['url'] if cats_data else None
    return image_url

def upload_image_to_calckey(image_url):
    # this section is the main area of bugs and issues qwq
    headers = {'Authorization': f'Bearer {calckey_api_key}'}
    data = {'url': image_url}
    response = requests.post(calckey_upload_url, json=data, headers=headers)
    if response.status_code == 204:
        return True
    return False

def get_most_recent_media_id():
    headers = {'Authorization': f'Bearer {calckey_api_key}'}
    data = {'limit': 1}
    response = requests.post(drive_files_url, json=data, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()[0].get('id')
    return None

def create_note_on_calckey(media_id):
    headers = {'Authorization': f'Bearer {calckey_api_key}'}
    data = {
        'text': 'Meet this adorable cat!',
        'mediaIds': [media_id]
    }
    response = requests.post(calckey_notes_url, json=data, headers=headers)
    return response.status_code

if __name__ == '__main__':
    while True:
        image_url = fetch_cat_image_url()
        if image_url:
            print("Image URL:", image_url)
            media_id = upload_image_to_calckey(image_url)
            if media_id:
                print("Uploaded image to calckey successfully. Media ID:", media_id)
                recent_media_id = get_most_recent_media_id()
                if recent_media_id:
                    status_code = create_note_on_calckey(recent_media_id)
                    if status_code == 200:
                        print('Note created successfully')
                    else:
                        print('Failed to create the note')
                else:
                    print("Failed to get the most recent media ID from calckey.")
            else:
                print("Failed to upload image to calckey.")
        else:
            print("Failed to fetch cat image URL from The Cat API.")
        # sleep owo
        time.sleep(120)
