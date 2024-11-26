#!usr/bin/env python
#-*- coding:utf-8 -*-

import time
import json
import scrapy
from ..items import NewsItem
from datetime import datetime


def parse_time(ctime):
    ctime = int(ctime)
    time_struct = time.strptime(time.ctime(ctime), '%a %b %d %H:%M:%S %Y')
    time_final = time.strftime("%Y-%m-%d %H:%M", time_struct)
    return time_final


class SohuSpider(scrapy.Spider):
    name = 'sohu'
    base_url = 'https://finance.sohu.com.cn/'
    cookies = {
        'SUV': '1723110003814ceoy7q',
        'gidinf': 'x099980107ee194733c49104f000429a71c39736c140',
        'reqtype': 'pc',
        '_dfp': '/0aMGlNEvaaNa/dalpImxj6CzZo1I3exk5m0bC+9kS4=',
        't': '1729926876480',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,eo;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.sohu.com',
        'Referer': 'https://www.sohu.com/xchannel/tag?key=%E6%96%B0%E9%97%BB-%E5%9B%BD%E9%99%85&scm=10001.581_14-201000.0.10005.0&spm=smpc.channel_114.block3_77_a6GaGx_1_nav.3.1729922887976CpeehLN_1523',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    # cate_kv = {
    #     "时政":{'pvId': '1729926876277_Pfr6p1C','pageId': '1729926876570_1723110003814c_TAz'},
    #     "国际":{'pvId': '1730017654549_1bmrXMR','pageId': '1730017654869_1723110003814c_CZ2'},
    #     "财经":{'pvId': '1730018890297_EJ4s5VA','pageId': '1730018890519_1723110003814c_fXr',},
    #     "科技":{'pvId': '1730020979677_LoFTKUC','pageId': '1730020979926_1723110003814c_Rkp',}
    # }


    with open(f"NewsSpider/url_kv/{name}.json", "r") as f:
        cate_kv = json.load(f)

    def __init__(self, category=None, time=None, *args, **kwargs):
        super(SohuSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.time = time

    def start_requests(self):
        start_page = 1
        end_page = 50
        cookies = {
            'SUV': '1723110003814ceoy7q',
            'gidinf': 'x099980107ee194733c49104f000429a71c39736c140',
            'reqtype': 'pc',
            '_dfp': '/0aMGlNEvaaNa/dalpImxj6CzZo1I3exk5m0bC+9kS4=',
            't': '1729926876480',
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,eo;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://www.sohu.com',
            'Referer': 'https://www.sohu.com/xchannel/tag?key=%E6%96%B0%E9%97%BB-%E5%9B%BD%E9%99%85&scm=10001.581_14-201000.0.10005.0&spm=smpc.channel_114.block3_77_a6GaGx_1_nav.3.1729922887976CpeehLN_1523',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        for page_num in range(start_page, end_page + 1):
            json_data = {
                'pvId': '1730017654549_1bmrXMR',
                'pageId': '1730017654869_1723110003814c_CZ2',
                'mainContent': {
                    'productType': '13',
                    'productId': '1524',
                    'secureScore': '50',
                    'categoryId': '47',
                    'adTags': '20000111',
                    'authorId': 121135924,
                },
                'resourceList': [
                    {
                        'tplCompKey': 'TPLFeedMul_2_9_feedData',
                        'isServerRender': False,
                        'isSingleAd': False,
                        'configSource': 'mp',
                        'content': {
                            'productId': '1649',
                            'productType': '13',
                            'size': 20,
                            'pro': '0,1',
                            'feedType': 'XTOPIC_SYNTHETICAL',
                            'view': 'feedMode',
                            'innerTag': 'channel',
                            'spm': 'smpc.channel_114.block3_77_O0F7zf_1_fd',
                            'page': page_num,
                            'requestId': f'1729926876383JEiiaXB_1524_{page_num}',
                        },
                        'context': {
                            'mkey': '',
                        },
                    },
                ],
            }
            
            if self.category:
                json_data.update(self.cate_kv[self.category])
                yield scrapy.Request(
                    url='https://odin.sohu.com/odin/api/blockdata',
                    method='POST',
                    headers=headers,
                    cookies=cookies,
                    body=json.dumps(json_data),
                    callback=self.parse,
                    meta={'page': page_num},
            )
            else:
                for cate in self.cate_kv.keys():
                    json_data.update(self.cate_kv[cate])
                    yield scrapy.Request(
                        url='https://odin.sohu.com/odin/api/blockdata',
                        method='POST',
                        headers=headers,
                        cookies=cookies,
                        body=json.dumps(json_data),
                        callback=self.parse,
                        meta={'page': page_num, 'cate': cate},
                    )


    def parse(self, response, **kwargs):
        if response.status != 200:
            return
        
        data_list = json.loads(response.text)['data']
        for data in data_list["TPLFeedMul_2_9_feedData"]["list"]:
            news_item = NewsItem()
            try:
                news_item['news_title'] = data['title']
                news_item["news_cover"] = data["cover"]
                news_item["news_brief"] = data["brief"]
                news_item['news_site'] = 'Sohu'
                # news_item['news_comments'] = data.get('comment_total', 0)
                # news_item['news_type'] = response.meta.get('cate')
                news_item['news_link'] = 'http://www.sohu.com' + data['url']
                print(news_item["news_title"])
            except KeyError:  # 其中一个原因：不是文章而是集合，所以没有authorId，authorName
                print(data_list.index(data))
                print(response.url)
                print(data)
                return
            if self.time and self.time not in news_item['news_time']:
                continue
            yield scrapy.Request(news_item['news_link'], self.parse_news, meta={'item': news_item}, dont_filter=True)

    def parse_news(self, response):
        news_item = response.meta.get('item')
        news_item['news_content'] = response.xpath('//*[@id="mp-editor"]//text()').extract()
        if not news_item['news_content']:
            news_item['news_content'] = response.xpath('//article[@class="article-text"]//p//text()').extract()
        cleaned_data = [item.strip() for item in news_item['news_content'] if item.strip()]
        remove_keywords = ['本文转自', '返回搜狐，查看更多', '责任编辑']
        cleaned_data = [item for item in cleaned_data if not any(keyword in item for keyword in remove_keywords)]
        news_item['news_content'] = ''.join(cleaned_data)
        news_item["news_img"] = response.xpath('//*[@id="mp-editor"]/p/img/@data-src').extract()
        news_item["news_time"] = response.xpath('//*[@id="news-time"]//text()').extract_first().strip()
        # news_item["news_time"] = datetime.strptime(news_item["news_time"], '%Y-%m-%d %H:%M')  # 将字符串转换为datetime对象

        yield news_item
