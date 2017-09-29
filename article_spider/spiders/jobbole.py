# -*- coding: utf-8 -*-
__author__ = 'Jeremy'

import scrapy
import re
from scrapy.http import Request
import sys
sys.path.append("../")
from article_spider import items
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        url_list = response.css("#archive .post-thumb a")
        for url_single in url_list:
            image_url = url_single.css("img ::attr(src)").extract_first('')
            web_page_url = url_single.css("::attr(href)").extract_first('')
            yield Request(url=web_page_url, callback=self.parse_detail, meta={'image_url': image_url})

        next_page_url = response.css("a.next.page-numbers ::attr(href)").extract_first()
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        # title = response.css(".entry-header h1::text").extract_first('')
        # create_date = response.css(".entry-meta-hide-on-mobile ::text").extract_first('').replace("·","").strip()
        # article_type = response.css(".entry-meta-hide-on-mobile a ::text").extract_first('')
        # praise_num = int(response.css(".vote-post-up h10 ::text").extract_first(''))
        #
        # fav_num = response.css(".bookmark-btn ::text").extract_first('')
        # match_result = re.match('.*?(\d+).*', fav_num)
        # if match_result:
        #     fav_num = int(match_result.group(1))
        # else:
        #     fav_num = 0
        #
        # comment_num = response.css("a[href='#article-comment'] span ::text").extract_first('')
        # match_result = re.match('.*?(\d+).*', comment_num)
        # if match_result:
        #     comment_num = int(match_result.group(1))
        # else:
        #     comment_num = 0

        # bole_items = items.ArticleSpiderItem()
        # bole_items['webpage_image_url'] = [webpage_image_url]
        # bole_items['title'] = title
        # bole_items['create_date'] = create_date
        # bole_items['article_type'] = article_type
        # bole_items['praise_num'] = praise_num
        # bole_items['fav_num'] = fav_num
        # bole_items['comment_num'] = comment_num

        #以下使用ItemLoader来提取处理数据，替代原来Item的作用
        webpage_image_url = response.meta['image_url']
        Itemloader_article = ItemLoader(item=items.ArticleSpiderItem(), response=response)
        Itemloader_article.add_css("title", ".entry-header h1::text")
        Itemloader_article.add_css("create_date", ".entry-meta-hide-on-mobile ::text")
        Itemloader_article.add_css("article_type", ".entry-meta-hide-on-mobile a ::text")
        Itemloader_article.add_css("praise_num", ".vote-post-up h10 ::text")
        Itemloader_article.add_css("fav_num", ".bookmark-btn ::text")
        Itemloader_article.add_css("comment_num", "a[href='#article-comment'] span ::text")
        Itemloader_article.add_value("webpage_image_url", webpage_image_url)
        article_itemloader = Itemloader_article.load_item() #将根据上面提供的规则进行数据解析，每一个解析的值都是以 list 结果的形式呈现，同时，将结果赋值 item

        # yield bole_items

        yield article_itemloader

        pass
