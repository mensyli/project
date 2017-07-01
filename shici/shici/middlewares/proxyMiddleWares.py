from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random

basedir = 'F:/Windows/Document/pycharm/proxy/result/alive_ip.txt'

class ProxyMiddleware(object):
	def process_request(self,request,spider):
		lines = open(basedir,'r').readlines()
		proxy = random.choice(lines)
		request.meta['proxy'] = "http://{}".format(proxy)