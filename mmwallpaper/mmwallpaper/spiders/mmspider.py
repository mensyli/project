# -*- coding: utf-8 -*-
import scrapy
from mmwallpaper.items import MmwallpaperItem

class MmspiderSpider(scrapy.Spider):
    name = "mmspider"
    allowed_domains = ["win4000.com"]
    start_urls = []

    for i in range(1,543):
        url = 'http://www.win4000.com/wallpaper_2285_0_0_{}.html'.format(str(i))
        start_urls.append(url)


    # 得到每页的图集列表
    def parse(self, response):
        atlas_list = response.xpath('//ul[@class="main-img clearfix"]/li')
        for list in atlas_list:
            atlas_url = list.xpath('./a/@href').extract()[0]
            atlas_name = list.xpath('./a/@title').extract()[0]
            yield scrapy.Request(atlas_url ,callback=self.get_image_list)




    # 得到图片列表
    def get_image_list(self, response):
        item = MmwallpaperItem()
        next_page=''
        try:
            image_list = response.xpath('//ul[@class="ulBigPic"]/li')
        except:
            image_list = response.xpath('//div[@class="pic-meinv pic-paper"]/a')
            next_page = response.xpath('//div[@class="pic-meinv pic-paper"]/a/@href').extract()[0]
        for list in image_list:
            image_url = list.xpath('./img/@src').extract()[0]
            title = list.xpath('./img/@title').extract()[0]
            # title = response.meta['atlas_name']
            item['title'] = title
            item['image_url'] = image_url
            yield item
        if next_page:
            yield scrapy.Request(next_page ,callback=self.get_image_list)

