import requests as reqs
import os
import sys

def main(name :str, fileList :list):
    for i, file in enumerate(fileList):
        url = file
        r = reqs.get(url)
        rstr = str(r.content)
   
        rstr = rstr[rstr.find('/streamta.pe/'):]
        link = rstr[:rstr.find('<')]
        rstr = rstr[rstr.find("xcdd"):]
        rstr = rstr[:rstr.find("\\")]
        rstr = rstr[-2:]
        link = 'https:/' + link[:-2] + rstr + '&stream=1'
        checkFile(f"./videos/{name}/{name}-{'0'*(4-(len(str(i+1))))}{i+1}.mp4")
        download(link, str(i+1), f"./videos/{name}/{name}-{'0'*(4-(len(str(i+1))))}{i+1}.mp4")
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
    t.pop(0)
    print(name)
    print(f"Episodes {len(t)}")
    print(t)
    checkFolder(name)
    main(name, t)
