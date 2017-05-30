# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class XatianqiSpider(scrapy.Spider):
    name = "XAtianqi"
    allowed_domains = ["tianqi.com"]
    start_urls = []
    citys = ['xian', 'baoji', 'lanzhou']
    for city in citys:
        start_urls.append('http://' + city + '.tianqi.com')

    def parse(self, response):
        '''
		date:今日日期
		week:星期
		img:天气图标
		temperature:当天温度
		weather:当天天气
		wind:当天风向
        '''

        items = []

        sixdays = response.xpath('//div[@class="tqshow1"]')

        for day in sixdays:
            item = WeatherItem()

            date = ''
            for datetitle in day.xpath('./h3//text()').extract():
                date += datetitle

            item['date'] = date
            item['week'] = day.xpath('./p//text()').extract()[0]
            item['img'] = day.xpath('./ul/li[@class="tqpng"]/img/@src').extract()[0]
            item['temperature'] = ''.join(day.xpath('./ul/li[2]//text()').extract())
            item['weather'] = day.xpath('./ul/li[3]//text()').extract()[0]
            item['wind'] = day.xpath('./ul/li[4]//text()').extract()[0]

            items.append(item)
        return items




