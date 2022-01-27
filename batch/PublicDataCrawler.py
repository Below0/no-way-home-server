import requests
from XmlParser import XmlParser
from ConfigManager import ConfigManager
from furl import furl
import mysql.connector

class PublicDataCrawler:
    def __init__(self, config, url='http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'):
        self.furl = furl(url)
        self.furl.args['serviceKey'] = config["service_key"]

    def run(self, date_id, region):
        target_furl = self.furl.copy()
        target_furl.args['DEAL_YMD'] = date_id
        target_furl.args['LAWD_CD'] = region
        
        res = requests.get(target_furl.url)
        decoded_content = res.content.decode(encoding='utf-8')

        return decoded_content

def generate_key(*args):
    return "|".join(args)

def split_key(k):
    return k.split("|")

class HcodeManager:
    def __init__(self, db_config):
        self.db = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["db"]
        )

        self.cursor = self.db.cursor()

    def get_hcodes(self, code):
        SQL = f"SELECT id, depth3 FROM full_region_info WHERE simple_id = {code}"
        self.cursor.execute(SQL)
        select_res = self.cursor.fetchall()

        region_name_dict = {depth3 : id for id, depth3 in select_res}
        return region_name_dict
        

if __name__ == "__main__":
    api_config = ConfigManager.get_config("open_api")
    db_config = ConfigManager.get_config("db")

    crawler = PublicDataCrawler(
        config=api_config
    )

    xml_parser = XmlParser()

    res = crawler.run(date_id='202012', region='11200')
    items = xml_parser.parse(res, ['거래금액', '아파트', '지번', '법정동'])

    apt_counter = {}
    apt_price_accumulator = {}
    
    for item in items:
        key = generate_key(item["법정동"], item["지번"], item["아파트"])

        cnt = apt_counter.get(key, 0)
        apt_counter[key] = cnt + 1

        total_price = apt_price_accumulator.get(key, 0)
        apt_price_accumulator[key] = total_price + int(item["거래금액"].replace(",", ""))

    hm = HcodeManager(db_config)
    codes = hm.get_hcodes('11200')
    print(codes)
    print(apt_price_accumulator)
    
