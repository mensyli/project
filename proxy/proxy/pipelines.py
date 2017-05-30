# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class ProxyPipeline(object):
    def process_item(self, item, spider):
        basedir = os.getcwd()
        filename1 = basedir + '/result/dxdlspider.txt'
        filename2 = basedir + '/result/kdlspider.txt'
        if spider.name == 'dxdlspider':
            content = item['address'].split('\r\n')
            for line in content:
                open(filename1,'a').write(line+'\n')
        elif spider.name == 'kdlspider':
        	open(filename2,'a').write(item['address'] + '\n')
        return item
