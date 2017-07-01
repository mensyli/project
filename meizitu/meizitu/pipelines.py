# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import re

class MeizituPipeline(object):
    def process_item(self, item, spider):

        basedir = 'F:/Images/temp/meizitu/'
        filename = re.findall(r'(\w+.(jpg|jpeg|png|bmp))$',item['img_url'])[0][0]
        if not os.path.exists(basedir + item['name']):
            os.makedirs(basedir + item['name'])

        with open(basedir + item['name'] + '/' +filename, 'wb') as f:
            f.write(requests.get(item['img_url']).content)
        return item
