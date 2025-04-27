import os
import requests
import cloudscraper#since cloudflare, we use cloudscraper
from tkinter import filedialog
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
#pick the link of the thread and the name of the foder that's gonna be made
thread_url = input('put the link of the thread')
if not thread_url:
    exit()
output_folder= input('name of the folder that u gonna make')
if not output_folder:
    output_folder='thread'
var = 0

#ask for the directory to create afolder
while var == 0:
    directory = filedialog.askdirectory(title='Select a directory')
    if directory:
        var=1
        a = input(f' u selected {directory}, wish to continue? yes or no')
        a = a.lower()
        if a == 'yes':
            break
        else:
            var=0
            continue
    else:
        print('select a directory')

#pick the diretory and open
new_path = os.path.join(directory, output_folder)
try:
    #make the folder
    os.mkdir(new_path)
    print('folder done')
except FileExistsError:
    print(f"folder already exists")
except Exception as e:
    print(f'error = {e}')

#get the html from the link
try:
    response = scraper.get(thread_url)
except requests.exceptions.ConnectionError as E:
    print(f'print error, non valid link')
    exit()
except Exception as d:
    print(d)

if response.status_code != 200:
    print(f'Failed to get the link')
    exit()
#image getter, create a bs4 object
soup = BeautifulSoup(response.text, 'html.parser')
#find all ocurrence of tag, a hlink(hyperlink), to download after, for every link
images = soup.find_all('a', class_='fileThumb')#get's the anchor of the hyperlink of the image, to check the class u need to go to the site, press f12 and use the mouse icon to see
if not images:
    print('not images found')
for image in images:
    #yeah
    image_url = 'https:' + image['href']#get's the real image"
    image_name = os.path.basename(image_url)#gets the number
    image_path = os.path.join(new_path, image_name)
    print(f'downloading {image_url}...')
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(image_response.content)#SINCE content gets bytes, and wb is write in bytes, yeah, and i need to put png or something like that before
            print(f'downloaded in {image_path}')
    else:
        print(f'failed to download {image_url}, status_code = {image_response.status_code}')

print('images downloaded')
