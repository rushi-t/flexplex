import os
import json
import requests
import string

BASE_URL = "http://flexplex.in/"
#BASE_URL = "http://localhost:8000/"
IMPRESSION_ACK_URL = BASE_URL + "hoarder/hoarding/hoarding_id/increment/campaign/campaign_id"

class CampaignPlaylist(object):
    current_item = -1
    total_items = 0

    def __init__(self, file_path):
        self._load_json(file_path)

    def _load_json(self, file_path):
        with open(file_path) as data_file:
            self.json_data = json.load(data_file)
            self.total_items = len(self.json_data['campaigns'])

    def get_next(self):
        if self.current_item < (self.total_items-1):
            self.current_item += 1
        else:
            self.current_item =0
        item = self.json_data['campaigns'][self.current_item]
        head, tail = os.path.split(item['resource'])
        self.send_impression_ack(self.json_data['id'],item['id'])
        return tail

    def send_impression_ack(self, hoarding_id, campaign_id):
        url = string.replace(IMPRESSION_ACK_URL, "hoarding_id", str(hoarding_id))
        url = string.replace(url, "campaign_id", str(campaign_id))
        r = requests.get(url)

    def length(self):
        return self.total_items;

def test_campaign_playlist(file_path):
    campaignPlaylist = CampaignPlaylist(file_path)
    count = 0
    while (count < 20):
        print str(count) + ", " + campaignPlaylist.get_next()
        count += 1

#test_campaign_playlist('campaign.json')