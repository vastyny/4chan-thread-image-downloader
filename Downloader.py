import os
import requests
from tkinter import filedialog
from bs4 import BeautifulSoup

#pick the link and the name of 
thread_url = input('put the link of the thread')
if not thread_url:
    exit()
output_folder= input('name of the folder')
if not output_folder:
    output_folder='thread'
var = 0
#ask for the directory
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

#get the link and the html
try:
    response = requests.get(thread_url)
except requests.exceptions.ConnectionError as E:
    print(f'print error, non valid link')
    exit()
except Exception as d:
    print(d)

if response.status_code != 200:
    print(f'Failed to get the link')
    exit()
#image getter, im not good at bs4
soup = BeautifulSoup(response.text, 'html.parser')
images = soup.find_all('a', class_='fileThumb')
if not images:
    print('not images found')
for image in images:
    image_url = 'https:' + image['href']
    image_name = os.path.basename(image_url)
    image_path = os.path.join(new_path, image_name)
    print(f'downloading {image_url}...')
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(image_response.content)
            print(f'downloaded in {image_path}')
    else:
        print(f'failed to download {image_url}, status_code = {image_response.status_code}')

print('images downloaded')
