# coding=utf-8
import requests
from lxml import html
import re
import os
import config
import threading
from time import ctime,sleep


def get_page_number(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    urls = []
    for i in selector.xpath("//ul/li/a/@href"):
        urls.append(i)
    return urls


def get_image_title(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_title = selector.xpath("//h2/text()")[0]
    return image_title

def get_image_amount(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    return image_amount


def get_image_detail_website(url):
    image_detail_websites = []
    image_amount = get_image_amount(url)
    for i in range(int(image_amount)):
        image_detail_link = '{}/{}'.format(url,i+1)
        response = requests.get(image_detail_link)
        if response.status_code == 200:
            selector = html.fromstring(response.content)
            image_download_link = selector.xpath("//div[@class='content']/a/img/@src")[0]
            image_detail_websites.append(image_download_link)
    return  image_detail_websites

def download_image(image_title, image_detail_websites):
    num = 1
    amount = len(image_detail_websites)
    path = 'F:/Images/temp/' + image_title
    for i in image_detail_websites:
        proxies = config.get_ips()
        for ip in proxies:
            proxy = {'http': ip.strip()}
            print(proxy)
            try:
                r = requests.get(url=i, headers=config.get_header(), proxies=proxy, timeout=3)
                if r.status_code == 200:
                    response = requests.get(url=i, headers=config.get_header(), proxies=proxy, timeout=3)
                    if response.status_code == 200:
                        if not os.path.exists(path):
                            os.makedirs(path)
                        os.chdir('F:/Images/temp/' + image_title)
                        filename = '%s%s.jpg' % (image_title, num)
                        print('正在下载图片：%s第%s/%s,' % (image_title, num, amount))
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        num += 1
                        break
                else:
                    continue
            except:
                print('该代理{}失效！'.format(proxy))

def get_imageset_page_number(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    imageset_amount = selector.xpath("//div[@class='page']/a[last()]/@href") # list
    total_number = re.findall(r"[0-9]{2}", "".join(imageset_amount)) # list
    return "".join(total_number)

def get_imageset_detail_websites(url):
    imageset_detail_websites = []
    imageset_amount = get_imageset_page_number(url)
    for i in range(int(imageset_amount)):
        imageset_detail_link = '{}/home/{}'.format(url, i+1)
        imageset_detail_websites.append(imageset_detail_link)
    return imageset_detail_websites

def download(url):
    url = url
    imageset_detail_websites = get_imageset_detail_websites(url)
    counter = 1
    page = 1
    for link in imageset_detail_websites:
        print("正在下载第%s页图集" % page)
        for i in get_page_number(link):
            print("正在下载图集%s" % counter)
            download_image(get_image_title(i), get_image_detail_website(i))
            counter += 1
        page += 1






# def get_proxy():
#     proxies = config.get_ips()
#     for ip in proxies:
#         proxy = {'http': ip.strip()}
#         try:
#             r = requests.get(url='http://www.baidu.com', headers=config.get_header(), proxies=config.get_ip(), timeout=3)
#             if r.status_code == 200:
#                return proxy
#             else:
#                 continue
#         except:
#             print('该代理{}失效！'.format(proxy))
#
#
#
# def multi_threading():
#     for i in range(1,2):
#         url = 'http://www.mmjpg.com/home/{}'.format(i)
#         print('****************************************正在下载第{}页'.format(i))
#         e = execute(url,i)
#         t = threading.Thread(target=e)
#         t.start()
#
# def execute(url,page):
#     gallery_list = get_every_page_gallery_list(url)
#     k =1
#     for gallery in gallery_list:
#         print('****************************************正在下载第{}页第{}个图集'.format(page,k))
#         # d = download_my_image(gallery,page,k)
#         # t = threading.Thread(target=d)
#         # t.start()
#         download_my_image(gallery, page, k)
#         k += 1
#
#
#
# def get_every_page_gallery_list(current_page_url=""):
#     pattern = "/html/body/div[2]/div[1]/ul/li/a/@href"
#     proxy = config.get_ip()
#     while True:
#         try:
#             response = requests.get(current_page_url, headers=config.get_header(), proxies=proxy)
#             if response.status_code == 200:
#                 selector = html.fromstring(response.content)
#                 gallery_list = selector.xpath(pattern)
#                 return gallery_list
#         except:
#             continue
#
#
#
# def download_my_image(gallery,page,num):
#
#     while True:
#         proxy1 = config.get_ip()
#         try:
#             response1 = requests.get(gallery, headers=config.get_header(), proxies=proxy1)
#             if response1.status_code == 200:
#                 selector = html.fromstring(response1.content)
#                 pattern_image = '//*[@id="content"]/a/img/@src'
#                 pattern_title = '//*[@id="content"]/a/img/@alt'
#                 pattern_total = '//*[@id="page"]/a[last()-1]/text()'
#                 total_page = selector.xpath(pattern_total)[0]
#                 image_title = selector.xpath(pattern_title)[0]
#                 k = 0
#                 for i in range(int(total_page)):
#                     image_url = gallery + '/' + str(k + 1)
#                     print(image_url)
#                     while True:
#                         proxy = config.get_ip()
#                         try:
#                             response = requests.get(image_url, headers=config.get_header(), proxies=proxy)
#                             if response.status_code == 200:
#                                 select = html.fromstring(response.content)
#                                 image = select.xpath(pattern_image)[0]
#                                 while True:
#                                     try:
#                                         resp = requests.get(image, headers=config.get_header(), proxies=proxy)
#                                         if resp.status_code == 200:
#                                             path = 'F:/Images/temp/' + image_title
#                                             if not os.path.exists(path):
#                                                 os.makedirs(path)
#                                             os.chdir('F:/Images/temp/' + image_title)
#                                             filename = '%s%s.jpg' % (image_title, k)
#                                             with open(filename, 'wb') as f:
#                                                 print(
#                                                     '****************************************正在下载第{}页第{}个图集图{}/{}'.format(
#                                                         page, num,
#                                                         k + 1,
#                                                         total_page))
#                                                 f.write(resp.content)
#
#                                     except:
#                                         continue
#
#                         except:
#                             continue
#                     k += 1
#
#         except:
#             continue



if __name__ == '__main__':
    download('http://www.mmjpg.com')