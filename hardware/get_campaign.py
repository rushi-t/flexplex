import urllib2
import json
from pprint import pprint
import wget
import urllib
import shutil
import time
import os
from subprocess import call

POLL_TIME = 1 * 60 #5 mins

def pollHoarding():
    response = urllib2.urlopen('http://148.72.245.147/hoarder/api/all/hoardings/1/')
    jsonData = json.load(response)
    saveHoarding(jsonData)

def saveHoarding(jsonData):
    with open('hoarding.json', 'r+') as file:
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
    call('rm -r resources/*', shell=True)
    response = urllib2.urlopen('http://148.72.245.147/hoarder/api/hoarding/1/campaigns/')
    data = json.load(response)
    for item in data:
        url = item['campaign']['resource']
        pprint(url)
        wget.download(url, out='resources')
        # urllib.urlretrieve(item['campaign']['resource'])
    print len(data)

# pollHoarding()

while True:
    print "Getting resources"
    pollHoarding()
    time.sleep(POLL_TIME)  # Delay for 1 minute (60 seconds)
