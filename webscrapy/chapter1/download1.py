import urllib2
import re
import itertools


def download(url, user_agent='wswp', num_retries=2):
	print 'Downloading:',url
	headers= {'User-Agent':user_agent}
	request = urllib2.Request(url,headers=headers)
	try:
		html = urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print 'Download error:',e.reason
		html = None
		if num_retries > 0:
			if hasattr(e,'code') and 500 <= e.code < 600:
				return download(url, user_agent, num_retries-1)
	return html


def crawl_sitemap(url):
	sitemap = download(url)
	links = re.findall('<loc>(.*?)</loc>',sitemap)
	for link in links:
		download(link)


def link_crawl():
	max_error = 5
	num_error = 0
	for page in itertools.count(1):
		url = 'http://example.webscraping.com/view/%d' % page
		html = download(url)
		if html is None:
			num_error += 1
			if num_error == max_error:
				break
		else:
			pass

if __name__ == '__main__':
	# download('http://httpstat.us/500',5)
	# download('http://www.meetup.com',5)
	# crawl_sitemap('http://example.webscraping.com/sitemap.xml')
	link_crawl()