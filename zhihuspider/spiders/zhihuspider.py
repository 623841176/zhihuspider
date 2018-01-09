# -*-coding:utf-8-*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import json
import re
import time


class zhihuspider(CrawlSpider):
    name = 'zhihuspider'
    start_urls = [
        'https://www.zhihu.com/api/v4/questions/53369195/answers?include=data%5B*%5D.is_normal%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos&offset=0&limit=20&sort_by=default']
    # start_urls = [
    #     'https://www.zhihu.com/api/v4/questions/53369195/answers?offset=0&limit=20&sort_by=default']
    cookie = 'd_c0="AECAGFRttAqPTs8Pk4tIkAnEWtpkEXsEfTw=|1476686947"; _zap=3074367f-2e99-44a7-a2b7-2a67de4aa742; hjstat_uv=3240106099524148887|679544; _ga=GA1.2.1614309345.1488466942; q_c1=ffbc865a5b774d08ba28817866fc433d|1508741548000|1476686947000; __utma=155987696.1614309345.1488466942.1510379985.1510379985.1; __utmz=155987696.1510379985.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); q_c1=ffbc865a5b774d08ba28817866fc433d|1512983427000|1476686947000; aliyungf_tc=AQAAAOnPrQnrMgAAOknndEo/T/ppcNdL; _xsrf=b6345542-6192-4b03-ba49-9815d46f854a; r_cap_id="ZjY5ZmQxYjAzNzVlNGQ2MDlkNTEzZjg3MzgyMTU5NWY=|1514525806|a3e0898468adb374df322b10f0be13512103cfe5"; cap_id="NWE5M2FkZDJiNzgzNGZjNjk5NzRjNDhhNmU1YWUwYzE=|1514525806|43cc0b2563a9b593146d82b933017f1080970c36"; l_cap_id="MWU5YjE1Yjk0OWExNDg0MDk3MGE5OWNmZDFhODEzNjQ=|1514525806|c439d8c17b598561329754eda571cde417f31d23"; capsion_ticket="2|1:0|10:1515485127|14:capsion_ticket|44:MDUyNDliNDdhOGQ2NDA1ZGFiMzc5YTczM2E2YjFiNDA=|e7af054e8150de44377d252bc46397c97873114ce0e89ea4c92fa4d0fd30cce2"; z_c0="2|1:0|10:1515485167|4:z_c0|92:Mi4xUXBaaEJnQUFBQUFBUUlBWVZHMjBDaVlBQUFCZ0FsVk43OFZCV3dDeFpwRVhJeEVVWWhzdGQwb0ZBV2lFZ1hIUC1R|82798a5e47748f286d66105c23806c73d7be769a613fc46e481a3bf5e70b8e0c"'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    offset = 20
    aftercookie = {}

    def start_requests(self):
        aftercookie = {}
        keyvalue = re.findall('([^; ].*?)="(.*?)"', self.cookie)
        # print(len(keyvalue))
        for i in range(len(keyvalue)):
            aftercookie[keyvalue[i][0]] = keyvalue[i][1]
        # print(aftercookie)
        self.aftercookie = aftercookie

        yield Request(url=self.start_urls[0], callback=self.parse, cookies=aftercookie, headers={
            'User-Agent': self.user_agent,
            'Cookie': aftercookie
        })

    def parse(self, response):
        data = json.loads(response.body)['data']
        print(data)
        for each in data:
            print(each['excerpt'], '\n')
        next_url = re.sub('offset=(.*?)&', 'offset=' + str(self.offset) + '&', self.start_urls[0])
        self.offset += 20
        print(next_url)
        time.sleep(0.3)
        if len(data) == 20:
            yield Request(url=next_url, callback=self.parse, cookies=self.aftercookie, headers={
                'User-Agent': self.user_agent,
                'Cookie': self.aftercookie
            })
