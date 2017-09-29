# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        print("here!!!")
        return item


class JsonWritePipeline(object):
    def open_spider(self, spider):
        self.file = open("items.j1", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)).encode("utf-8").decode("unicode-escape") + "\n"
        # line = line.encode()
        self.file.write(line)
        return item


class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['webpage_image_url']:
            yield Request(url=image_url)

    def item_completed(self, results, item, info):
        pass


class JsonExporterPipeline(object):

    def __init__(self):
        """
        先打开文件，传递一个文件
        """
        self.file = open('articleexporter.json', 'wb')
        #调用 scrapy 提供的 JsonItemExporter导出json文件
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_close(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CsvExporterPipeline(object):
    def open_spider(self, spider):
        self.file = open('article_csv_exporter.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding="utf-8")

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.file.close()

