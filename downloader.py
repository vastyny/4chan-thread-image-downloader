import cloudscraper as cs
import os
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog
import time

scraper = cs.create_scraper()

def getfiles():
    how_many = 0
    certain = 0
    try:
        thread_url = input("what's the link of the thread")
        if thread_url:
            response = scraper.get(thread_url)
            response.raise_for_status()
            while certain == 0:
                path = os.path.join(filedialog.askdirectory(title="which directory is going to save from?"))
                cer = input(f"do you wanna save in {path}?(y/n)")
                if cer.lower() == "y":
                    certain = 1
            soup = BeautifulSoup(response.text, "lxml")
            for i in soup.find_all("a", class_="fileThumb"):
                if not i:
                    raise Exception("no images")
                images = "https:" + i["href"]
                image_name = os.path.basename(images)
                image_path = os.path.join(path, image_name)
                if os.path.exists(image_path):
                    print("already exists")
                    continue
                print(f"downloading image, link = {images}")
                image_response = scraper.get(images)
                if image_response.status_code == 200:
                    with open(image_path, "wb") as file:
                        file.write(image_response.content)
                        print(f"downloaded")
                        how_many+=1
                        print(how_many)
                else:
                    print(f"failed to download {image_url}, status_code = {image_response.status_code}")
            print(f"{how_many} total images")
            time.sleep(10)
    except Exception as e:
        print(e)
if __name__ == "__main__":
    getfiles()
