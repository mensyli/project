# -*- coding: utf-8 -*-
import scrapy
import re
from xiezhen.items import XiezhenItem

class XiezhenspiderSpider(scrapy.Spider):
    name = "xiezhenspider"
    allowed_domains = ["5857.com"]
    start_urls = []

    for i in range(1,43):
        start_urls.append('http://www.5857.com/list-9--3437----{}.html'.format(str(i)))

    def parse(self, response):
        
        gallery_prefix = response.xpath('//div[@class="piclist"]/ul[@class="clearfix"]/li')
        print('此页共含有{}个图集'.format(len(gallery_prefix)))

        for gallery in gallery_prefix:
            gallery_url = gallery.xpath('./div/a/@href').extract()[0]
            gallery_name = gallery.xpath('./div/a/@title').extract()[0]
            print('图集名称为{},图集地址为{}'.format(gallery_name,gallery_url))
            yield scrapy.Request(gallery_url,meta={'gallery_name':gallery_name},callback=self.get_gallery_list)

    def get_gallery_list(self, response):
        
        max_page = response.xpath('//div[@class="photo"]/div[@class="page"]/a[last()-1]//text()').extract()[0]
        print('图集{}共含有{}张图片'.format(response.meta['gallery_name'], int(max_page)))
        
        first_page_url = response.url

        for i in range(1,int(max_page)+1):
            page_url = re.findall(r'(.+)\.html$',first_page_url)[0] + '_' + str(i) + '.html'
            middle = re.findall(r'(_\d+)\.html$',page_url)[0]
            if middle == '_1':
                page_url = re.sub(r'(_\d+)\.html$','',page_url) + '.html'
            print('图片名称为{},图片页面为{}'.format(response.meta['gallery_name'], page_url))
            yield scrapy.Request(page_url,meta={'gallery_name':response.meta['gallery_name'],'page_url':page_url},callback=self.get_image_url)


    def get_image_url(self, response):

        image_urls = response.xpath('//div[@class="photo"]/a[@class="photo-a"]/img/@src').extract()
        gallery_name = response.meta['gallery_name']
        page_url = response.meta['page_url']
        print('当前页面的地址为'.format(page_url))
        item = XiezhenItem()
        item['gallery_name'] = gallery_name

        for image_url in image_urls:
            item['image_url'] = image_url
            print('当前图片名称为:{}，图片地址为:{}'.format(gallery_name, image_url))
            yield item