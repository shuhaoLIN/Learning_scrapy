# -*- coding: utf-8 -*-

import re

import scrapy
from scrapy.http import Request

from getjs.items import GetjsItem
from selenium import webdriver

import time
from scrapy.http import Request

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
driver.get("http://item.jd.com/25007267199.html")
driver.execute_script(js)
time.sleep(10)  # 等待JS执行
print driver.page_source

