# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
import codecs
import pymysql

class WeatherPipeline(object):
	def process_item(self, item, spider):
		'''
		处理从spider传过来的数据
		将数据保存到文本
		'''

		basedir = os.getcwd()
		filename = basedir + '/data/weather.txt'

		with open(filename, 'a') as f:
			f.write(item['date'] + '\n')
			f.write(item['week'] + '\n')
			f.write(item['temperature'] + '\n')
			f.write(item['weather'] + '\n')
			f.write(item['wind'] + '\n')

		with open(basedir + '/data/' + item['date'] + '.png', 'wb') as f:
			f.write(requests.get(item['img']).content)

		return item


class Weather2Json(object):
	def process_item(self, item, spider):
		'''
		将数据保存到json
		'''

		basedir = os.getcwd()
		filename = basedir + '/data/weather.json'

		with codecs.open(filename, 'a') as f:
			line = json.dumps(dict(item), ensure_ascii = False) + '\n'
			f.write(line)

		return item


class Weather2Mysql(object):
	'''
	将数据保存到数据库
	'''

	def process_item(self, item, spider):
		date = item['date']
		week = item['week']
		img = item['img']
		temperature = item['temperature']
		weather = item['weather']
		wind = item['wind']

		connection = pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = '*********',
			password = '***********',
			db = 'scrapyDB',
			charset = 'utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)

		try:
			with connection.cursor() as cursor:
				sql = '''
					INSERT INTO WEATHER(date, week, temperature, weather, wind, img) 
						VALUES (%s, %s, %s, %s, %s, %s)
				'''
				cursor.execute(sql,(date, week, temperature, weather, wind, img))
			connection.commit()

		finally:
			connection.close()


		return item
