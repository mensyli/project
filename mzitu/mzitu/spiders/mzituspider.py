# -*- coding: utf-8 -*-
import scrapy
from mzitu.items import MzituItem

class MzituspiderSpider(scrapy.Spider):
    name = "mzituspider"
    allowed_domains = ["mzitu.com"]
    start_urls = []

    for i in range(1,145):
        start_urls.append('http://www.mzitu.com/page/' + str(i) + '/')

    def parse(self, response):
        atlas_list = response.xpath('//ul[@id="pins"]/li')
        print('此页共含有{}个图集'.format(len(atlas_list)))
        for list in atlas_list:
            atlas_url = list.xpath('./a/@href').extract()[0]
            atlas_name = list.xpath('./span/a//text()').extract()[0]
            print('图集{}地址为{}'.format(atlas_name,atlas_url))
            yield scrapy.Request(atlas_url,meta={'name':atlas_name},callback=self.get_every_atlas_urls)

    def get_every_atlas_urls(self,response):
        max_num = response.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()').extract()[0]
        print('这个图集共含有{}个图片'.format(int(max_num)))
        for i in range(1,int(max_num)+1):
            page_url = response.url + '/' + str(i)
            print('图片页面地址为{}'.format(page_url))
            yield scrapy.Request(page_url,meta={'name':response.meta['name']},callback=self.get_image_url)


    def get_image_url(self,response):
        item = MzituItem()
        item['name'] = response.meta['name']
        image_urls = response.xpath('//div[@class="main-image"]/p/a/img/@src').extract()
        for image_url in image_urls:
            item['image_url'] = image_url
            yield item