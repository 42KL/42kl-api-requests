import requests
from PIL import Image

# File generated with users/get_users_picture_url.py
with open('users_pictures_links.txt', 'r') as f:
    links = f.read().splitlines()
    for link in links:
        print(link)
        er_n = 0
        while er_n < 3:
            try:
                img = Image.open(requests.get(link, stream = True).raw, mode='r')
                img.save(f'img/{link.split("/")[-1]}')
                print(f"run {er_n} for {link.split('/')[-1]}")
                break
            except Exception as err:
                print(err)
                er_n += 1
            
            
