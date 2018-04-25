# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

import sys
import os
#设置工程目录os.path.abspath(__file__)就是当前main文件的路径
#os.path.driname(os.path.abspath(__file__))  父目录
#以便进行调试
print os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","GETJS"])