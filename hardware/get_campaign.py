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

POLL_TIME = 1 * 30 #5 mins
BASE_URL = 'http://148.72.245.147/'
RESOURCE_DIR = 'resources'
HOARDING_JSON = 'hoarding.json'
HOARDING_ID = str(1)
HOARDING_URL = BASE_URL +'hoarder/api/all/hoardings/' + HOARDING_ID
HOARDING_CAMPAIGNS_URL = BASE_URL +'hoarder/api/hoarding/' + HOARDING_ID + '/campaigns'


def pollHoarding():
    pprint(HOARDING_URL)
    response = urllib2.urlopen(HOARDING_URL)
    jsonData = json.load(response)
    saveHoarding(jsonData)

def saveHoarding(jsonData):
    with open(HOARDING_JSON, 'r+') as file:
        fileData = file.read()
        if fileData != '':
            fileJson = json.loads(fileData)
            if fileJson['last_update'] != jsonData['last_update']:
                downloadResources()
                file.seek(0)
                json.dump(jsonData, file)
                file.truncate()
        else:
            downloadResources()
            file.seek(0)
            json.dump(jsonData, file)
            file.truncate()

def downloadResources():
    #call('rm -r resources/*', shell=True)
    #pprint(HOARDING_CAMPAIGNS_URL)
    response = urllib2.urlopen(HOARDING_CAMPAIGNS_URL)
    data = json.load(response)
    for item in data:
        url = item['campaign']['resource']
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
