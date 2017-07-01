# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import re


class QikkPipeline(object):
    def process_item(self, item, spider):
        
        base = 'F:/Images/temp/qikk/' 

        image_name = item['image_name']
        image_url = item['image_url']

        basedir = base + image_name + '/'
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        filename = re.findall(r'(\w+.(jpg|jpeg|png|bmp))$',image_url)[0][0]

        fullpath = basedir + filename
        if not os.path.exists(fullpath):
            with open(fullpath, 'wb') as f:
                f.write(requests.get(image_url).content)

        return item
