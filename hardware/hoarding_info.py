import os
import json
import requests
import string


class HoardingInfo(object):
    h_res = 1920
    v_res = 1080

    def __init__(self, file_path):
        self._load_json(file_path)

    def _load_json(self, file_path):
        with open(file_path) as data_file:
            json_data = json.load(data_file)
            self.h_res = json_data['h_res']
            self.v_res = json_data['v_res']


def test_hoarding_info(file_path):
    hoardingInfo = HoardingInfo(file_path)
    print str(hoardingInfo.h_res) + "x" +str(hoardingInfo.v_res)


test_hoarding_info('hoarding.json')