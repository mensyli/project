# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import requests
import re

class XiezhenPipeline(object):
    def process_item(self, item, spider):
        
        basedir = 'F:/Images/temp/xiezhen/'
        
        gallery_name = item['gallery_name']
        image_url = item['image_url']
        
        path = basedir + gallery_name + '/'

        if not os.path.exists(path):
            os.makedirs(path)
        
        filename = re.findall(r'(\w+.(jpg|jpeg|png|bmp))$',image_url)[0][0]
        fullpath = path + filename
        if not os.path.exists(fullpath):
            with open(fullpath, 'wb') as f:
                f.write(requests.get(image_url).content)
        return item
