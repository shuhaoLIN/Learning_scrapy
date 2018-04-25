# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetjsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()


    next_Link = scrapy.Field()  # 进入商品详细信息页面
    # 商品详细信息页面的标签
    brand = scrapy.Field()  # 品牌
    shop = scrapy.Field()  # 店铺
    Gross_weight = scrapy.Field()  # 毛重
    Commodity_name = scrapy.Field()  # 商品名称
    Commodity_number = scrapy.Field()  # 商品编号
    labels = scrapy.Field()  # 标题
    price = scrapy.Field()  # 价格
    commit_times = scrapy.Field()  # 评价次数
    image_url = scrapy.Field()  # 图片的url
    image_addr = scrapy.Field()  # 图片保存的本地地址



    pass
