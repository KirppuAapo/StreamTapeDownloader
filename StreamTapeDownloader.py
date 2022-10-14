import requests as reqs
import os
import sys

def main(fileList :list):

    for i, file in enumerate(fileList):
        url = file
        name = url.split('/')
        if name[-1] == '':
            name.pop(-1)
        name = name[-1]

        r = reqs.get(url)
        rstr = str(r.content)
   
        rstr = rstr[rstr.find('/streamta.pe/'):]
        link = rstr[:rstr.find('<')]
        rstr = rstr[rstr.find("xcdd"):]
        rstr = rstr[:rstr.find("\\")]
        rstr = rstr[-2:]
        link = 'https:/' + link[:-2] + rstr + '&stream=1'
        checkFile(f"./videos/{name}.mp4")
        download(link, str(i+1), f"./videos/{name}.mp4")
        sys.stdout.write(f"\nFile {i+1} download complete\n")
    print("All downloads are complete")


def download(url, fileIndex, fileName):
    with open(fileName, "wb") as w:
        print('File opened')
        r = reqs.get(url, stream=True)
        total = int(r.headers.get("content-length"))
        downloaded = 0
        sys.stdout.write(f"Downloading file {fileIndex} from {url}\n")
        for data in r.iter_content(chunk_size=max(int(total/1000), 1024*1024)):    
            downloaded += len(data)
            percentage = int((downloaded/total)/0.02)
            sys.stdout.write(f'\r[{"*"*percentage}{"."*(50-percentage)}]')
            w.write(data)

def checkFolder(name :str):
    try:
        os.makedirs(f"./videos/{name}")
    except:
        pass

def checkFile(name :str):
    if not(os.path.isfile(name)):
        with open(name, "x"):
            pass

with open ("STToDownload.txt", "r") as t:
    t = t.read().split("\n")
    name = t[0]
    if t[-1] == '':
        t.pop(-1)
    print(t)
    checkFolder('./videos/')
    main(t)
