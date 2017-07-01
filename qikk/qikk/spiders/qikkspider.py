# -*- coding: utf-8 -*-
import scrapy
from qikk.items import QikkItem


class QikkspiderSpider(scrapy.Spider):
    name = "qikkspider"
    allowed_domains = ["7kk.com"]
    start_urls = []
    for i in range(1,168):
        start_urls.append('http://www.7kk.com/bizhi/meinv/new----{}.html'.format(str(i)))

    def parse(self, response):
        page_urls = response.xpath('//div[@id="container"]/div[@class="grid"]')
        print('此页共含有{}张图'.format(len(page_urls)))

        for page in page_urls:
            page_url = 'http://www.7kk.com' + page.xpath('./div[@class="imgholder"]/a/@href').extract()[0]
            page_name = page.xpath('./div[@class="ksGirl"]/label[@class="lblTitle"]/text()').extract()[0]
            print('图片名称为{},页面地址为{}'.format(page_name,page_url))
            yield scrapy.Request(page_url,meta={'page_name':page_name},callback=self.get_image_url)

    def get_image_url(self, response):
        image_url = response.xpath('//dl[@class="wallpaper-down clearfix"]/dd/a[last()]/@href').extract()[0]
        image_name = response.meta['page_name']
        print('图片名称为{},图片地址为{}'.format(image_name,image_url))
        item = QikkItem()
        item['image_url'] = image_url
        item['image_name'] = image_name
        yield item