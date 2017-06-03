# -*- coding: utf-8 -*-
import scrapy
import re
from uumnt.items import UumntItem

class UumntspiderSpider(scrapy.Spider):
    name = "uumntspider"
    allowed_domains = ["uumnt.com"]
    start_urls = []
    
    start_urls.append('http://www.uumnt.com/meinv')
    for i in range(2,411):
        start_urls.append('http://www.uumnt.com/meinv/list_{}.html'.format(str(i)))

    def parse(self, response):
        atlas_list = response.xpath('//div[@id="mainbodypul"]/div')
        print('此页有{}个图集'.format(len(atlas_list)))
        for list in atlas_list:
            atlas_name = list.xpath('./a/@title').extract()[0]
            atlas_url = 'https://www.uumnt.com' + list.xpath('./a/@href').extract()[0]
            print('图集{}地址为{}'.format(atlas_name,atlas_url))
            yield scrapy.Request(atlas_url, meta={'name':atlas_name}, callback = self.get_every_atlas_images)


    def get_every_atlas_images(self, response):
        print('进入图集.................................................')
        total = response.xpath('//div[@class="page"]/a[last()]/@href').extract()[0]
        total_num = re.findall(r'(\d+)\.html$',total)[0]
        print('此图集共有{}张图片'.format(int(total_num)))
        for i in range(1,int(total_num)+1):
            subfix = re.findall(r'(\d+).html$',response.url)[0] + '_' + str(i) + '.html'
            middle = re.findall(r'(\w+)\/\d+\.html$',response.url)[0]
            pic_url = 'https://www.uumnt.com/' + middle + '/' + subfix
            print('图片页面地址为{}'.format(pic_url))
            yield scrapy.Request(pic_url,meta={'name':response.meta['name']},callback=self.get_every_image)


    def get_every_image(self, response):
        print('下载图片..................................................')
        item = UumntItem()
        item['name'] = response.meta['name']
        image_urls = response.xpath('//div[@class="bg-white p15 center imgac clearfix"]/a/img/@src').extract()
        for image_url in image_urls:
            item['image_url'] = image_url
            yield item
