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
from spiders.common import parse_item_info, parse_tweet_info, parse_long_tweet


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
            yield Request(url, callback=self.parse_user)

    def parse_user(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        print(f'\n\n---data---\n{data}\n\n')
        item = parse_item_info(data['data']['user'])
        print(f'\n\n---item---\n{item}\n\n')

        # get post content
        url = f"https://weibo.com/ajax/statuses/mymblog?uid={item['_id']}&page=1"
        yield Request(url, callback=self.parse_post, meta={'item': item, 'page_num': 1})


    def parse_post(self, response, **kwargs):
        item = response.meta['item']
        data = json.loads(response.text)
        tweets = data['data']['list']
        for tweet in tweets:
            tweet_item = parse_tweet_info(tweet)
            if tweet_item['isLongText']:
                url = "https://weibo.com/ajax/statuses/longtext?id=" + tweet_item['mblogid']
                yield Request(url, callback=parse_long_tweet, meta={'item': item})
            else:
                item['post_content'] = tweet_item
                yield item
        if tweets:
            user_id, page_num = response.meta['item']['_id'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page={page_num}"
            yield Request(url, callback=self.parse_post, meta={'item': item, 'page_num': page_num})