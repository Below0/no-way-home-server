from ConfigManager import ConfigManager
from PublicDataCrawler import PublicDataCrawler, HcodeManager
from GeoCoder import NaverGeoCoder
from XmlParser import XmlParser
import mysql.connector
import json
import sys

SQL_APT_UPSERT = """
    INSERT INTO apt_info (apt_name, address, lat_lon, avg_price, updated_date)
    VALUES (%s, %s, ST_GeomFromText('POINT(%s %s)'), %s, NOW())
    ON DUPLICATE KEY UPDATE address=%s
"""

db_config = ConfigManager.get_config("db")

db = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"],
    database=db_config["db"]
)

cursor = db.cursor()


def generate_key(*args):
    return "|".join(args)


def split_key(k):
    return k.split("|")


def run(date_id='202101', city_name='서울특별시'):
    naver_config = ConfigManager.get_config("naver_api")
    db_config = ConfigManager.get_config("db")
    open_api_config = ConfigManager.get_config("open_api")

    crawler = PublicDataCrawler(open_api_config)
    hm = HcodeManager(db_config)
    simple_hcodes = hm.get_city_codes(city_name)
    xml_parser = XmlParser()

    for hcode in simple_hcodes:
        res = crawler.run(date_id=date_id, region=hcode)
        items = xml_parser.parse(res, ['거래금액', '아파트', '지번', '법정동'])

        apt_counter = {}
        apt_price_accumulator = {}

        for item in items:
            key = generate_key(item["법정동"], item["지번"], item["아파트"]).strip()

            cnt = apt_counter.get(key, 0)
            apt_counter[key] = cnt + 1

            total_price = apt_price_accumulator.get(key, 0)
            apt_price_accumulator[key] = total_price + int(item["거래금액"].replace(",", ""))

        print(apt_price_accumulator)

        hm = HcodeManager(db_config)
        full_hcode_dict = hm.get_hcodes(hcode)
        print(full_hcode_dict)

        gc = NaverGeoCoder(naver_config)

        apts = []

        for k, v in apt_price_accumulator.items():
            region, block_id, apt_name = split_key(k)
            stripped_region = region.strip()

            avg_price = v // apt_counter[k]

            full_hcode = full_hcode_dict[stripped_region]
            query = f"{region} {block_id}"

            geo = gc.transform(full_hcode, query)
            geo_dict = json.loads(geo)
            apt_geo_info = geo_dict['addresses'][0]
            apt_address = apt_geo_info['roadAddress']
            lon = float(apt_geo_info['x'])
            lat = float(apt_geo_info['y'])

            apt_info = [apt_name, apt_address, lon, lat, avg_price, apt_address]  # Unique Key 용도로 apt_address 2번 삽입

            apts.append(apt_info)

        for apt in apts:
            cursor.execute(SQL_APT_UPSERT, apt)

        db.commit()


if __name__ == "__main__":
    city_name = sys.argv[1]
    print(city_name)

    run();
