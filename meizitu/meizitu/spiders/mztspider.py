# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem

class MztspiderSpider(scrapy.Spider):
    name = "mztspider"
    allowed_domains = ["mmjpg.com"]
    start_urls = []

    for i in range(1,68):
        start_urls.append('http://www.mmjpg.com/home/' + str(i))

    def parse(self, response):
        atlas_list = response.xpath('//div[@class="pic"]/ul/li')
        print('此页共含有{}个图集'.format(len(atlas_list)))
        for li in atlas_list:
            atlas_url = li.xpath('./a/@href').extract()[0]
            atlas_name = li.xpath('./a/img/@alt').extract()[0]
            print('图集{}地址为{}'.format(atlas_name,atlas_url))
            yield scrapy.Request(atlas_url, meta={'name':atlas_name},callback=self.get_every_atlas_page)
    
    def get_every_atlas_page(self,response):
        max_page = response.xpath('//div[@class="page"]/a[last()-1]//text()').extract()[0]
        print('这个图集共含有{}个图片'.format(int(max_page)))
        for i in range(1,int(max_page)+1):
            page_url = response.url + '/' + str(i)
            print('图片页面地址为{}'.format(page_url))
            yield scrapy.Request(page_url,meta={'name':response.meta['name']},callback=self.get_every_image_url)


    def get_every_image_url(self,response):
    	item = MeizituItem()
    	item['name'] = response.meta['name']
    	image_url = response.xpath('//div[@class="content"]/a/img/@src').extract()[0]
    	item['img_url'] = image_url
    	yield item