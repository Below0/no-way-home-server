import requests
from XmlParser import XmlParser
from ConfigManager import ConfigManager
from furl import furl


class GeoCoder:
    def transform(self):
        pass

class NaverGeoCoder(GeoCoder):
    URL = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'

    def __init__(self, config):
        self.header = {
            "X-NCP-APIGW-API-KEY-ID": config["client_id"],
            "X-NCP-APIGW-API-KEY": config["client_key"]
            }

    def transform(self, h_code, address):
        data = {
            "query" : address,
            "filter" : f"BCODE@{h_code};",
        }
        
        res = requests.get(NaverGeoCoder.URL, headers=self.header, params=data)
        decoded_content = res.content.decode(encoding='utf-8')
        return decoded_content


if __name__ == "__main__":
    naver_config = ConfigManager.get_config("naver_api")
    gc = NaverGeoCoder(naver_config)
    