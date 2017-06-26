import urllib2
import json
from pprint import pprint
import wget
import urllib
import shutil
import time
import os
from subprocess import call
import os.path
import sys

POLL_TIME = 1 * 30 #5 mins
# BASE_URL = 'http://148.72.245.147/'
BASE_URL = 'http://localhost:8000/'
# PATH = '/home/pi/work/hardware/'
PATH = '/mnt/sda4/work/django/flexplex/hardware/'
RESOURCE_DIR = PATH + 'videos'
HOARDING_JSON = PATH + 'hoarding.json'
HOARDING_ID = str(5)
HOARDING_URL = BASE_URL +'hoarder/api/all/hoardings/' + HOARDING_ID

def pollHoarding():
    try:
        pprint(HOARDING_URL)
        response = urllib2.urlopen(HOARDING_URL)
        jsonData = json.load(response)
        saveHoarding(jsonData)
    except:
        print("Exception while getting Ads", sys.exc_info()[0])

def saveHoarding(jsonData):
    with open(HOARDING_JSON, 'r+') as file:
        fileData = file.read()
        if fileData != '':
            fileJson = json.loads(fileData)
            if fileJson['last_update'] != jsonData['last_update']:
                downloadResources(jsonData['campaigns'])
                file.seek(0)
                json.dump(jsonData, file)
                file.truncate()
        else:
            downloadResources(jsonData['campaigns'])
            file.seek(0)
            json.dump(jsonData, file)
            file.truncate()

def downloadResources(campaigns):
    for campaign in campaigns:
        url = campaign['resource']
        head, tail = os.path.split(url)
        if os.path.exists(RESOURCE_DIR+'/'+tail):
            pprint('Skipping: ' + tail)
        else:
            pprint('Downloading: ' + tail)
            wget.download(url, out=RESOURCE_DIR)
    pprint("----------------------------------------------------------------")
        # urllib.urlretrieve(item['campaign']['resource'])

# Create empty json if doesn't exists
open(HOARDING_JSON, 'a').close()

while True:
    print "Getting resources"
    pollHoarding()
    time.sleep(POLL_TIME)  # Delay for 1 minute (60 seconds)