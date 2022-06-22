from types import NoneType
import requests
from bs4 import BeautifulSoup
from sys import argv
import json
import os
import time

"""Bobylev Yaroslav 2022 / boyara.best@gmail.com"""

print("Hello, this is anime images parser")

for i in argv:
    pass

good_thing = {";" : "%3B", ":":"%3a", ",":"%2c", "%":"%25"}


chunk_size = 512 * 1024  # to download normally

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"

LANGUAGE = "en-US,en;q=0.5"

sess = requests.session()
    
sess.headers['USER-AGENT'] = USER_AGENT
sess.headers['LANGUAGE'] = LANGUAGE

config = json.load(open("config.json"))


if input(f"Do you want to check {config['link']} availability? (yes/no)  ") == "yes":
    request = requests.get(config["link"])
    if str(request) != "<Response [200]>":
        print("Check your VPN/Network status. Status code is", request.status_code)
    else:
        print(f'{config["link"]} is available')

task = input("whose photos do you want?  ")
if task == "":
    if input("You didn't give a name. Want to get a random response? (yes/no)  ") != "yes":
        print("Unfortunately I have no choice :(")
    task == "all"

tas_spl = "_".join(task.split())
for i in good_thing:
    tas_spl.replace(i, good_thing[i])

count = int(input("how many images do you need to download? (-2 to one page/ -1 to infinite number)  "))

output_path = input(f"in which directory should we place the folder '{task}' with the result?   ")

pth = os.path.join(output_path, tas_spl)

#  creating dir
if not (os.path.exists(pth)):
    os.mkdir(pth)

im_sess = requests.session()

im_sess.headers['USER-AGENT'] = USER_AGENT
im_sess.headers['LANGUAGE'] = LANGUAGE


def download_in_dir(path, link, num):
    print("link:", link)
    time.sleep(1)
    image_page = BeautifulSoup(im_sess.get(link).content, 'lxml')
    im_name = tas_spl + f" [{num}]"
    main_ = image_page.find('div', class_="mainBodyPadding")
    
    try:
        download_link = str(main_.find('picture').find("img")["src"])
    except:
        download_link = str(main_.find('video').find("source")["src"])
    print(f"downloading   {download_link}", end="")

    down_req = requests.get(download_link)
    res = download_link[len(download_link) - download_link[::-1].index('.')::]
    f = open(f"{path}/{im_name}.{res}", "wb")
    for ch in down_req.iter_content(chunk_size=chunk_size):
        f.write(ch)
    f.close()

    print("     Done.")



pid = 0 # every page pid + 42 (больше становится нахуй пошел)
n = 0

if count == -1:
    cycle = True
elif count == -2:
    cycle = (pid == 0)
else:
    cycle = (n < count)

while cycle:
    time.sleep(1)
    link = str(config["example_link"] + tas_spl + "&pid=" + str(pid))
    request = sess.get(link)
    if request.status_code != 200:
        print("downloaded all images. Good luck!")
        quit()

    soup = BeautifulSoup(request.content, "lxml")

    images_container = soup.find("div", class_="thumbnail-container")
        

    if images_container == "None":
        print("Can't find images using this link")
        quit()
    else:
        for i in images_container.find_all('article', class_="thumbnail-preview"):

            time.sleep(1)
            image_preview_link = i.find('a')['href']
            download_in_dir(pth, image_preview_link, n)
            n += 1
        if len(images_container.find_all('article', class_="thumbnail-preview")):
                print("downloaded all images. Good luck.")
                quit()

    pid += 42
print("All images are downloaded. Good luck!")
