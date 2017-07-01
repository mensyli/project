# -*- coding: utf-8 -*-
import scrapy
from shici.items import ShiciItem


class ShicispiderSpider(scrapy.Spider):
    name = "shicispider"
    allowed_domains = ["www.shicimingju.com"]
    start_urls = ['http://www.shicimingju.com/']

    # 得到朝代列表
    def parse(self, response):
        dynast_urls = response.xpath('//*[@id="left"]/div[1]/ul/li')
        for list  in dynast_urls:
            dynast_url = 'http://www.shicimingju.com' + list.xpath('./a/@href').extract()[0]
            dynast_name = list.xpath('./a/text()').extract()[0]
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print('当前朝代为:{},网址为：{}'.format(dynast_name,dynast_url))
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            yield scrapy.Request(dynast_url,meta={'dynast_name':dynast_name},callback=self.get_current_dynast_shier_list)

    # 得到诗人列表
    def get_current_dynast_shier_list(self, response):
            shier_urls = response.xpath('//div[@class="shirenlist"]/ul/li')
            for list in shier_urls:
                try:
                    shier_url = 'http://www.shicimingju.com' + list.xpath('./a/@href').extract()[0]
                    try:
                        shier_name = list.xpath('./a/text()').extract()[0]
                    except:
                        shier_name = '无名氏'
                    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    print('当前朝代为:{},当前诗人为:{},网址为：{}'.format(response.meta['dynast_name'],shier_name,shier_url))
                    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    yield scrapy.Request(shier_url, meta={'dynast_name':response.meta['dynast_name'],'shier_name':shier_name},
                        callback=self.get_shi_list)
                except:
                    pass
            try:
                next_url = 'http://www.shicimingju.com' + response.xpath('//div[@class="pagenavi yuanjiao"]/span/a[last()]/@href').extract()[0]
                next_name = response.xpath('//div[@class="pagenavi yuanjiao"]/span/a[last()]/text()').extract()[0]
                if next_name == '下一页':
                    yield scrapy.Request(next_url,meta={'dynast_name':response.meta['dynast_name']},
                        callback=self.get_current_dynast_shier_list)
            except:
                pass

    # 得到诗词列表
    def get_shi_list(self, response):
        shi_list = response.xpath('//div[@class="shicilist"]/ul/li[1]')
        for list in shi_list:
            try:
                shi_url = 'http://www.shicimingju.com' + list.xpath('./a/@href').extract()[0]
                shi_name = list.xpath('./a/text()').extract()[0]
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print('当前朝代为:{},当前诗人为:{},当前诗名为:{},网址为：{}'.
                    format(response.meta['dynast_name'],response.meta['shier_name'],shi_name,shi_url))
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                yield scrapy.Request(shi_url,meta={'dynast_name':response.meta['dynast_name'],
                    'shier_name':response.meta['shier_name'],'shi_name':shi_name},callback=self.get_shi)
            except:
                pass
        try:
            next_url = 'http://www.shicimingju.com' + response.xpath('//div[@class="pagenavi yuanjiao"]/span/a[last()]/@href').extract()[0]
            next_name = response.xpath('//div[@class="pagenavi yuanjiao"]/span/a[last()]/text()')[0]
            if next_name == '下一页':
                yield scrapy.Request(next_url,meta={'dynast_name':response.meta['dynast_name'],
                       'shier_name':response.meta['shier_name']},callback=self.get_shi_list)
        except:
            pass


    # 得到诗词
    def get_shi(self, response):
        try:
            shici_content = response.xpath('//div[@class="shicineirong"]/text()').extract()
            shici_shangxi = response.xpath('//div[@class="shangxi yuanjiao"]/text()').extract()
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(response.meta['shier_name'] + response.url)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(shici_content)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(shici_shangxi)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        except:
            shici_shangxi = ''
        if not shici_content:
            shici_content = response.xpath('//div[@class="shicineirong"]/p/text()').extract()
        dynast_name = response.meta['dynast_name']
        shier_name = response.meta['shier_name']
        if '*' in shier_name:
            shier_name = shier_name.replace('*','_')
        shi_name = response.meta['shi_name']

        item = ShiciItem()
        item['dynast'] = dynast_name
        item['author'] = shier_name
        item['title'] = shi_name
        item['body'] = shici_content
        item['shangxi'] = shici_shangxi
        yield item
