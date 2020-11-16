'''
@author Tejas Valame
Date: 16Nov2020
Lives in: Pune,India
'''
import string, re, os, sys
from bs4 import BeautifulSoup as bs
import requests as rq


def end(i):
    input("Exception: "+ str(i)+"\nHit Enter to EXIT")
    exit()

def cd():	#creates a directory to store our downloaded files
    try:
        os.mkdir(name+"-"+dict1[qty])
        print("Created New Directory: ", name+"-"+dict1[qty])
    except FileExistsError:
        print("Continuing to download in Existing Folder: ", name)
    except:
        print("Cant create directory")
        end("dir creation error")

def parser(url1, txt):	#parses the hml and reurns url that contains txt
    pg=rq.get(url1)
    
    if(pg.status_code!=200):
        print("HTTP Error, Code", str(pg.status_code))
        return None
    else:
        soup=bs(pg.text, 'html.parser')
        for anchor in soup.find_all('a', href=True):
            h=anchor.get('href', None)
            if re.search(txt,h)!=None:
                return h
    return None
def correct(str):	#formats the input from line 77 to correct URL [Valid inputs 'death note', 'https://gogoanime.so/death-note-episode-1', 'death-note', 'https://gogoanime.so/category/death-note']
    str=str.replace(" ", "-")
    if re.search("https://gogoanime.+?/category/.+", str)!=None:
        return str
    if re.search("https://gogoanime.+?/.+-episode-", str)!=None:
        str=re.findall("https://gogoanime.+?/(.+)-episode-", str)[0]
    return "https://gogoanime.so/category/"+str

def store(url): #saves the files in folder
    print("Download Link:",url)
    response = rq.get(url, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None: # no content length header
        print("no content length header")
        #eps+=1
    else:
        file_name = name+"-"+dict1[qty]+"/"+name+"-episode-"+str(ep_num) +"."+response.headers.get('content-type').split('/')[1]
        with open(file_name, "wb") as f:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
        #epf+=1
                







dict1={ 1:"360p", 2:"480p", 3:"720p", 4:"1080p", }
epf=0
eps=0
baseURL=correct(input("Enter the Base URL from gogo anime: "))

try:
    base_ep=int(input("Enter episode number to begin with: "))
    end_ep=int(input("Enter episode number to end with: "))
    if base_ep>end_ep:
        end("Wrong Numbers")
    print("Menu:\n 1: 360p\t 2: 480p\t 3: 720p\t 4: 1080p")
    qty=int(input("Enter Episode Download Quality:"))
    if(qty not in range(1,5)):
        end("Undefined Quality")
except:
    end("Baka")
lst=baseURL.split('/')
name=lst[4]

cd()
try:
    for ep_num in range(base_ep, end_ep+1):
        print("\nDownloading ",name," ep ",str(ep_num))
        ep_URL=lst[0]+"//"+lst[2]+'/'+lst[4]+"-episode-"+str(ep_num)
        print("Episode URL:", ep_URL)
        dpg=parser(ep_URL, "https://gogo-stream.com/download")
        if(dpg==None):
            print("Could not access dgp: ", ep_URL, "Moving Next")
            epf+=1
            continue
        print(name,"episode", str(ep_num),":",dpg)
        dl=parser(dpg, dict1[qty])
        if(dl==None):
            print("Could not access dl: ", "Moving Next")
            epf+=1
            continue
        else:
            store(dl.replace("amp;", ""))
    print(eps, "Succeded", epf, "failed")
    input("\nDownload Completed.\n Happy Watching\nHit Enter to Exit")
except Exception:
    print(eps, "Succeded", epf, "Failed")
    input("\nSome Fatal Error has occured\nHit Enter to Exit")
