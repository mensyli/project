# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import re


class MmwallpaperPipeline(object):
    def process_item(self, item, spider):

        basedir = 'F:/Images/temp/mmwallpaper/'
        title = item['title']
        image_url = item['image_url']
        path = basedir + title + '/'
        
        if not os.path.exists(path):
            os.makedirs(path)

        filename = re.findall(r'(\w+.(jpg|jpeg|png|bmp))$',item['image_url'])[0][0]

        fullpath = path + filename

        if not os.path.exists(fullpath):
            with open(fullpath,'wb') as f:
                f.write(requests.get(image_url).content) 
        return item
