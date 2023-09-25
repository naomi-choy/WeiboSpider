#!/usr/bin/env python
# encoding: utf-8
"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_item_info


class CustomSpider(Spider):
    """
    微博用户信息爬虫
    """
    name = "custom_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        """
        爬虫入口
        """
        # 这里user_ids可替换成实际待采集的数据
        user_ids = ['5978791676']
        urls = [f'https://weibo.com/ajax/profile/info?uid={user_id}' for user_id in user_ids]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        print(f'\n\n\n---unparsed data---\n{data}')
        item = parse_item_info(data['data']['user'])
        url = f"https://weibo.com/ajax/profile/detail?uid={item['_id']}"
        yield Request(url, callback=self.parse_detail, meta={'item': item})

    @staticmethod
    def parse_detail(response):
        """
        解析详细数据
        """
        item = response.meta['item']
        data = json.loads(response.text)['data']
        print(f'\n\n\n----reponse data---\n{data}\n\n\n')
        print(f'----item----\n{item}\n\n\n')

        yield item
