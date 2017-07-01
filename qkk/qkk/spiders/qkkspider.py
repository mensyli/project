# -*- coding: utf-8 -*-
import scrapy
import re
from qkk.items import QkkItem


class QkkspiderSpider(scrapy.Spider):
    name = "qkkspider"
    allowed_domains = ["7kk.com"]
    start_urls = []
    for i in range(1,11):
        start_urls.append('http://www.7kk.com/meinv/xinggan/new----{}.html'.format(str(i)))

    def parse(self, response):
        gallery_list =  response.xpath('//div[@class="beatyCon"]/ul[@class="beautyUl clear"]/li')
        print('此页共含有{}张图集'.format(len(gallery_list)))

        for gallery in gallery_list:
            gallery_url = 'http://www.7kk.com' + gallery.xpath('./a[1]/@href').extract()[0]
            gallery_name = gallery.xpath('./a[last()]/text()').extract()[0]
            print('图集名称为{},图集地址为{}'.format(gallery_name,gallery_url))
            yield scrapy.Request(gallery_url,meta={'gallery_name':gallery_name},callback=self.get_image_list)
    
    def get_image_list(self, response):
        max_page = response.xpath('//div[@id="bottompage"]/div[@id="pageList"]/a[@class="last"]/text()').extract()[0]
        print('图集{}共含有{}页'.format(response.meta['gallery_name'], int(max_page)))

        first_page_url = response.url
        
        for page in range(1, (int(max_page))+1):
           
            page_url = re.findall(r'(.+)\.html$',first_page_url)[0] + '-' + str(page) + '.html'
            print('图集名称为{},当前图集页面地址为{}'.format(response.meta['gallery_name'], page_url))
            yield scrapy.Request(page_url,meta={'gallery_name':response.meta['gallery_name']},callback=self.get_image_page_url)

    def get_image_page_url(self, response):
        image_list = response.xpath('//div[@id="container"]/div[@class="grid"]')
        page_image_num = len(image_list)
        print('此页共含有{}张图片'.format(page_image_num))

        current_image = 0
        for image in image_list:
            current_image += 1
            page_image_url = 'http://www.7kk.com' + image.xpath('./div[@class="imgholder"]/a/@href').extract()[0]
            page_image_name = response.meta['gallery_name']
            print('将要下载的页面为{}'.format(response.url))
            print('当前图片名称为:{}，图片页面地址为:{},是{}/{}'.format(page_image_name, page_image_url,current_image,page_image_num))
            yield scrapy.Request(page_image_url,meta={'page_image_name':page_image_name,'current_image':current_image,'page_image_num':page_image_num,'current_Gallery_page':response.url},callback=self.get_image_url)

    def get_image_url(self, response):
        image_url = response.xpath('//div[@class="img_wrapper"]/div[@class="imgbox"]/a[1]/@href').extract()[0]
        image_name = response.meta['page_image_name']
        current_image = response.meta['current_image']
        page_image_num = response.meta['page_image_num']
        current_Gallery_page = response.meta['current_Gallery_page']
        print('正在下载的页面为{}'.format(current_Gallery_page))
        print('当前图片名称为:{}，图片地址为:{},正在下载{}/{}'.format(image_name, image_url,current_image,page_image_num))
        item = QkkItem()
        item['image_url'] = image_url
        item['image_name'] = image_name
        yield item