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
#BASE_URL = 'http://148.72.245.147/'
BASE_URL = 'http://192.168.0.107:8000/'
PATH = '/home/pi/work/hardware/'
#PATH = '/mnt/sda4/work/django/flexplex/hardware/'
RESOURCE_DIR = PATH + 'videos'
HOARDING_JSON = PATH + 'hoarding.json'
CAMPAIGN_JSON = PATH + 'campaign.json'
HOARDING_ID = str(7)
HOARDING_URL = BASE_URL +'hoarder/api/all/hoardings/' + HOARDING_ID
HOARDING_CAMPAIGNS_URL = BASE_URL +'hoarder/api/hoarding/' + HOARDING_ID + '/campaigns'


def pollHoarding():
    try:
        pprint(HOARDING_URL)
        response = urllib2.urlopen(HOARDING_URL)
        jsonData = json.load(response)
        saveHoarding(jsonData)
    except:
        print "Exception while getting Ads"

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

    with open(CAMPAIGN_JSON, 'r+') as file:
        file.seek(0)
        json.dump(data, file)
        file.truncate()
        file.close()

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