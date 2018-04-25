# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
from scrapy.pipelines.images import ImagesPipeline

class GetjsPipeline(object):
    def process_item(self, item, spider):
        return item

class CSV(object):
    def __init__(self):
        self.file = codecs.open('goods.csv','w',encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 转成字符串，ensure_ascii能够让中文正常显示
        self.file.write(lines)
        return item


class JsonWithEncodingPipline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8")
    #打开json文件
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)+"\n"
        #转成字符串，ensure_ascii能够让中文正常显示
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()
        #在spider结束后进行关闭文件


class JDImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):   #重载这个函数进行对图片的路径进行保存
        for ok,value in results:
            image_file_path = value["path"]  #因为有可能是多个result

        #image_file_path = results[0][1]['path']
        item['image_addr'] = image_file_path
        return item
        #返回item给下一个pipeline函数进行调用