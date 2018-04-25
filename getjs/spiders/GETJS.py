# -*- coding: utf-8 -*-
import re

import scrapy

from getjs.items import GetjsItem
from selenium import webdriver

import time
from scrapy.http import Request

def get_all(str5 , num):
    js = """
        function scrollToBottom() {

            var Height = document.body.clientHeight,  //文本高度
                screenHeight = window.innerHeight,  //屏幕高度
                INTERVAL = 50,  // 滚动动作之间的间隔时间
                delta = 500,  //每次滚动距离
                curScrollTop = 0;    //当前window.scrollTop 值

            var scroll = function () {
                curScrollTop = document.body.scrollTop;
                window.scrollTo(0,curScrollTop + delta);
            };

            var timer = setInterval(function () {
                var curHeight = curScrollTop + screenHeight;
                if (curHeight >= Height){   //滚动到页面底部时，结束滚动
                    clearInterval(timer);
                }
                scroll();
            }, INTERVAL)
        }
        scrollToBottom()
        """

    driver = webdriver.PhantomJS()  # 获取浏览器对象
    driver.get(str5)
    driver.execute_script(js)
    time.sleep(num)  # 等待JS执行
    return driver.page_source



class GetjsSpider(scrapy.Spider):
    name = 'GETJS'
    #allowed_domains = ['https://search.jd.com/Search?keyword=%E9%BC%A0%E6%A0%87&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%BC%A0%E6%A0%87&psort=2&click=0']
    start_urls = [
        'https://search.jd.com/Search?keyword=%E9%BC%A0%E6%A0%87&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%BC%A0%E6%A0%87&psort=2&click=0/',
        'https://search.jd.com/Search?keyword=%E9%BC%A0%E6%A0%87&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E9%BC%A0%E6%A0%87&psort=2&page=3&s=61&click=0'
    ]


    def parse(self, response):
        # response._encoding='utf-8'
        new_body = get_all(response.url, 20)
        response = response.replace(body=new_body)   #将response的body变换成为我们想要的加载了js后的body
        # response._set_body(new_body)
        goods = response.xpath('//*[@id="J_goodsList"]/ul/li[@class="gl-item"]')
        for each in goods:
            next_Link = each.xpath('div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@href').extract_first()  # 下一页url
            print "进去！！"
            next_Link = "http:"+next_Link
            print next_Link
            yield Request(url=next_Link,callback=self.next_parse)
            # request = Request(url=next_Link, callback=self.next_parse)
            # request.meta['PhantomJS'] = True
            # yield request

    def next_parse(self,response):
        print "进来了！"
        # response.encoding('utf-8')
        #print response.body
        item = GetjsItem()
        item["next_Link"] = response.url

        response = response.replace(body=get_all(response.url, 10))

        price = response.xpath('/html/body/div[5]/div/div[2]/div[3]/div/div[1]/div[2]/span[1]/span[2]/text()|//div[@class="summary-price J-summary-price"]/div[@class="dd"]/span[1]/span/text()').extract() #价格


        brand = response.xpath('//*[@id="parameter-brand"]/li/a/text()').extract()[0]  # 品牌

        Commodity_name = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[1]/text()').extract()[0]  # 商品名称
        Commodity_name = re.match(u"商品名称：.*?(.*)", Commodity_name).group(1)  #匹配出来内容

        Commodity_number = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[2]/text()').extract()[0]  # 商品编号
        Commodity_number = re.match(".*?(\d+).*", Commodity_number).group(1)    #匹配出来内容

        shop = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[3]/a/text()').extract()[0]  # 店铺

        Gross_weight = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[4]/text()').extract()[0]  # 毛重
        Gross_weight = re.match(u"商品毛重：?(.*)",Gross_weight).group(1)   #匹配毛重信息

        labels = response.xpath('/html/body/div[5]/div/div[2]/div[1]/text()|/html/body/div[7]/div/div[2]/div[1]/text()|/html/body/div[7]/div/div[2]/div[1]/text()').extract()[0]  # 标题
        labels = labels.replace(' ',"").replace('\n',"")   #去除空格以及换行符等

        commit_times = response.xpath('//*[@id="comment-count"]/a/text()').extract()[0]  # 评价次数

        image_url = response.xpath('//*[@id="spec-img"]/@src').extract()[0]  # 图片的url

        image_url = "http:" + image_url
        item["price"] = price
        item["brand"] = brand
        item["Commodity_name"] = Commodity_name
        item["Commodity_number"] = Commodity_number
        item["shop"] = shop
        item["Gross_weight"] = Gross_weight
        item["labels"] = labels
        item["commit_times"] = commit_times
        item["image_url"] = [image_url]

        yield item


