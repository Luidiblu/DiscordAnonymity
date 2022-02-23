import requests
import time
import string
import random
from dotenv import load_dotenv, find_dotenv
from random import randrange
from wget import download
import os
import json
import base64


def get_gif():
    '''
    This method should get a random gif from Giphy API.
    '''
    r = requests.get(
        'https://api.giphy.com/v1/gifs/random',
        params={
            'api_key': os.getenv('giphy_api_key'), 
        }
    )
    return json.loads(r.text)['data']['images']['original']['url']


def save_gif(gif):
    '''
    This method saves a gif in /tmp folder
    '''
    print(gif)
    name = f"discord_{randrange(100000000)}.gif"
    download(gif, out=f'/tmp/{name}')
    return f'/tmp/{name}'


def encode_string(gif_path):
    '''
    This method receives a path containing a gif file, and encode to base64
    in order to generate a datauri
    '''
    with open(gif_path, 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return f"""data:application/octet-stream;base64,{encoded_string.decode()}"""


def get_gif_path():
    '''
    Just a marshaller to organize the gif path
    '''
    gif = get_gif()
    return save_gif(gif)


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    '''
    This method generates a random nickname with 16 characters
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def make_request():
    '''
    This script makes the "all the fuck"
    Calls those methods above and request a patch to Discord API
    '''
    avatar_path = get_gif_path()
    encoded_avatar_string = encode_string(avatar_path)
    banner_path = get_gif_path()
    encoded_banner_string = encode_string(banner_path)
    r = requests.patch(
       'https://discordapp.com/api/v9/users/@me',
        headers={'authorization': os.getenv('discord_token'), 'content-type': 'application/json'},
        data=json.dumps({'username': id_generator(),
              'email': os.getenv('discord_email'),
              'password': os.getenv('discord_password'),
              'avatar': encoded_avatar_string,
              'banner': encoded_banner_string,
              'discriminator': os.getenv('discord_discriminator'),
              'new_password': None}))

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    if os.getenv('WORKING') == 'luidiblu':
        while True:
            print('Changing Discord info!')
            make_request()
            print('Sleeping...')
            time.sleep(1800000)
