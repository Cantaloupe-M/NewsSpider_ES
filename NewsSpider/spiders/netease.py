#!usr/bin/env python
# -*- coding:utf-8 -*-

import json
import scrapy
import re
from ..items import NewsItem
import time

def parse_time(ctime):
    time_struct = time.strptime(ctime, '%m/%d/%Y %H:%M:%S')
    time_final = time.strftime("%Y-%m-%d %H:%M", time_struct)
    return time_final


class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    base_url = 'http://news.163.com/'

    # 将 cookies 格式化为字典
    cookies = {
        'Qs_lvt_382223': '1723109578%2C1723196264',
        'Qs_pv_382223': '1410631857528691700%2C1661359657171768300',
        '_ntes_nnid': '2195eb0651290af5f618fdcc191147c8,1726213025331',
        '_ntes_nuid': '2195eb0651290af5f618fdcc191147c8',
        'NTES_PASSPORT': '5Dr.lATybR2Tr88BTVDpgH9hyrJoPQu8yaLcYlKRJVSCWh3VWELSHaN4QBTR7_6jwTQRPQGnS_kbDB_sBmnPkU5qBQE8ycyLu2BmuucdcXKenrwwKSAZoM0Ys21WjndxnhjgTlgk9P2ILGpJ6vhKt4iNWfV1ExR_MZb53QJHz00NNHcQ35E1vSm3.eZUmHij5ylX6Ff0zUUCa',
        'timing_user_id': 'time_QGUmInbGEr',
        '_ntes_origin_from': '',
        's_n_f_l_n3': '607610fcf3a134c11730686596436',
        'pver_n_f_l_n3': 'a',
        'UserProvince': '%u5168%u56FD',
        'ne_analysis_trace_id': '1730702033169',
        '_antanalysis_s_id': '1730702443230',
        'NTES_PC_IP': '%E4%B8%9C%E4%BA%AC%7C%E6%97%A5%E6%9C%AC',
        'vinfo_n_f_l_n3': '607610fcf3a134c1.1.1.1730099509816.1730099825553.1730702693887',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,eo;q=0.7',
        'referer': 'https://news.163.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    custom_settings = {'REDIRECT_ENABLED': False}

    with open(f"NewsSpider/url_kv/{name}.json", "r") as f:
        cate_kv = json.load(f)

    def __init__(self, category=None, time=None, *args, **kwargs):
        super(NeteaseSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.time = time

    def start_requests(self):
        params = {'callback': 'data_callback'}

        if self.category:
            base_urls = list(self.cate_kv.get(self.category).values())
        else:
            base_urls = []
            for category, subcategories in self.cate_kv.items():
                for subcategory, link in subcategories.items():
                    base_urls.append(link)

        for base_url in base_urls:
            for i in range(1, 6):
                if i==1:
                    formatted_url = base_url.format("")
                else:
                    formatted_url = base_url.format("_"+f"{i:02d}")
                yield scrapy.Request(
                    url=formatted_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    cb_kwargs={'params': params},
                    meta={'category': self.category}
                )


    def parse(self, response,  **kwargs):
        print(response.url)
        if response.status != 200:
            return
        json_str = re.search(r'data_callback\((.*)\)', response.text, re.DOTALL).group(1)
        data_list = json.loads(json_str)
        # with open("netease.json","w") as f:
        #     json.dump(data_list,f,ensure_ascii=False,indent=4)
        for data in data_list:
            news_item = NewsItem()
            news_item["news_comments"] = data["tienum"]
            news_item["news_cover"] = data["imgurl"]
            news_item["news_keywords"] = [d["keyname"] for d in data["keywords"]]
            news_item["news_link"] = data['docurl']
            news_item["news_media"] = data.get("source","")
            news_item["news_site"] = "Netease"
            news_item["news_time"] = parse_time(data['time'])
            news_item['news_title'] = data['title']
            yield scrapy.Request(url=news_item["news_link"], headers=self.headers, cookies=self.cookies, callback=self.parse_news, meta={'news_item': news_item})
        
    def parse_news(self, response,**kwargs):
        news_item = response.meta['news_item']
        news_item["news_content"] = response.xpath("/html/body/div[2]/div[2]/div[3]/div[2]/p//text()").getall()
        news_item["news_img"] = response.xpath("/html/body/div[2]/div[2]/div[3]/div[2]/p//img/@src").getall()
        yield news_item
