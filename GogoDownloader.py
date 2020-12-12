'''
@author Tejas Valame
Date: 16Nov2020
Lives in: Pune,India
Get the exe here: https://mega.nz/file/ZDxkFIrS#DKX04SdhZDzG4h2xDcFdkqoPuK0SP_LZ4O65ZrxCgrg
*Only works on win 64 bit*
'''

import re, os, sys
from bs4 import BeautifulSoup as bs
import requests as rq

def end(i):
    input("Exception: " +str(i) +"\nHit Enter to EXIT")
    exit()

def cd():	#creates a directory to store our downloaded files
    try:
        os.mkdir(name+"-"+dict1[qty])
        print("Created New Directory:", name +"-" +dict1[qty])
    except FileExistsError:
        print("Continuing to download in Existing Folder:", name+"-"+dict1[qty])
    except:
        end("dir creation error")

def parser(url1, txt1):	#parses the page of given url and reurns link that contains txt
    pg=rq.get(url1)
    
    if(pg.status_code!=200):
        print("HTTP Error, Code:", pg.status_code)
        return None
    soup=bs(pg.text, 'html.parser')
    for anchor in soup.find_all('a', href=True):
        h=anchor.get('href', None)
        if(txt1 in h):
            return h
    return None
    
def correct(str):	
#formats the input from line 77 to correct URL 
# [Valid inputs 'death note', 'https://gogoanime.so/death-note-episode-1', 
# 'death-note', 'https://gogoanime.so/category/death-note']
    str=str.strip().replace(" ", "-")
    if re.search("https://gogoanime.+?/category/.+", str)!=None:
        return str
    if re.search("https://gogoanime.+?/.+-episode-", str)!=None:
        str=re.findall("https://gogoanime.+?/(.+)-episode-", str)[0]
    return "https://gogoanime.so/category/"+str

def store(url): #saves the files in folder
    print("Download Link:",url,"\n\n")
    response = rq.get(url, stream=True, timeout=10)
    total_length = response.headers.get('content-length')

    if total_length is None: # no content length header
        print("no content length header")
    else:
        file_name = name+"-"+dict1[qty]+"/"+name+"-"+dict1[qty]+"-episode-"+str(ep_num) +"."+response.headers.get('content-type').split('/')[1]
        with open(file_name, "wb") as f:
            dl = 0
            total_length = int(total_length)
            print("Download Size:",int(total_length/1048576)+1, "MB")
            for data in response.iter_content(chunk_size=5120):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                #The following line displays download percentage and progress bar
                sys.stdout.write("\r["+'=' * done+' ' * (50-done)+"] "+str(dl/1048576)[:6]+" MB/"+str(total_length/1048576)[:6]+ " MB "+str(dl/total_length*100)[:5]+"%" )   
                sys.stdout.flush()
dict1={ 1:"360p", 2:"480p", 3:"720p", 4:"1080p", }
epf=0
baseURL=correct(input("Enter the URL from gogo anime: "))

try:
    base_ep=int(input("Enter episode number to begin with: "))
    end_ep=int(input("Enter episode number to end with: "))
    if base_ep>end_ep:
        end("Wrong Numbers")
    print("Menu:\n 1: 360p\t 2: 480p\t 3: 720p\t 4: 1080p")
    qty=int(input("Enter Episode Download Quality: "))
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
        dpg=parser(ep_URL, "download")
        if(dpg==None):
            print("Could not access download page:", ep_URL, "Try it manually. Moving Next")
            epf+=1
            continue
        print(name,"episode", str(ep_num),":",dpg)
        dl=parser(dpg, dict1[qty])
        if(dl==None):
            print(name+"-episode-"+str(ep_num), "is not available in", dict1[qty]+". Try some other resolution. Moving Next")
            epf+=1
            continue
        else:
            try:
                store(dl.replace("amp;", ""))
            except Exception:
                epf+=1
    print("\n"+str(end_ep-base_ep-epf+1), "Succeded", epf, "failed")
    input("\nDownload Completed.\n Happy Watching\nHit Enter to Exit")
except Exception as ex:
    print("Exception",ex)
    input("\nHit Enter to Exit")
