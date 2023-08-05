import requests

cat_api_url = 'https://api.thecatapi.com/v1/images/search?limit=1'
calckey_upload_url = 'https://calckey.example/api/drive/files/upload-from-url'

# replace with actual keys, qwq
cat_api_key = ''
calckey_api_key = ''

def fetch_cat_image_url():
    headers = {'x-api-key': cat_api_key}
    response = requests.get(cat_api_url, headers=headers)
    cats_data = response.json()
    image_url = cats_data[0]['url'] if cats_data else None
    return image_url

def upload_image_to_calckey(image_url):
    headers = {'Authorization': f'Bearer {calckey_api_key}'}
    data = {'url': image_url}
    response = requests.post(calckey_upload_url, json=data, headers=headers)
    if response.status_code == 204:
        return True
    return False

if __name__ == '__main__':
    image_url = fetch_cat_image_url()
    if image_url:
        print("Image URL:", image_url)
        if upload_image_to_calckey(image_url):
            print("Uploaded image successfully.")
        else:
            print("Failed to upload image.")
    else:
        print("Failed to fetch cat image URL from The cat API.")
