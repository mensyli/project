# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import re
class MzituPipeline(object):
    def process_item(self, item, spider):
        basedir = 'F:/Images/temp/mzitu/'
        filename = re.findall(r'\w+.jpg$',item['image_url'])[0]
        if not os.path.exists(basedir + item['name']):
            os.makedirs(basedir + item['name'])
        with open(basedir + item['name'] + '/' + filename, 'wb') as f:
            f.write(requests.get(item['image_url']).content)
        return item 
