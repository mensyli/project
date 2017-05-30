
import setting
import requests
import config
from lxml import html
import time

def get_dxdlspider():
    url = setting.url
    time.sleep(2)
    content = requests.get(url=url, headers=config.get_header()).content.decode()
    path = setting.save_ip + 'a1.txt'
    with open(path,'a') as f:
        f.write(content+'\n')


def get_kdlspider():
    pattern_ip = '//*[@id="list"]/table/tbody/tr/td[1]/text()'
    pattern_port = '//*[@id="list"]/table/tbody/tr/td[2]/text()'
    start_url = []
    path = setting.save_ip + 'a2.txt'
    ip_port_list = []
    for i in range(1,42):
        time.sleep(2)
        url = 'http://www.kuaidaili.com/free/inha/'+ str(i) + '/'
        start_url.append(url)
    for i in start_url:
        print(i)
        time.sleep(2)
        response = requests.get(url=i, headers=config.get_header())
        content = response.content
        selector = html.fromstring(content)
        ip = selector.xpath(pattern_ip)
        port = selector.xpath(pattern_port)
        for i in zip(ip, port):
            ip_port = i[0]+':'+i[1]
            ip_port_list.append(ip_port)
    with open(path, 'a') as f:
        f.write('\n')
        for i in ip_port_list:
            f.write(i+'\n')


def get_xicidailispinder():
    url = 'http://www.xicidaili.com/'
    ip_port_list = []
    path = setting.save_ip + 'a3.txt'
    for i in range(4):
        k = 0
        for j in range(19):
            time.sleep(2)
            num = j + 3 + k
            pattern_ip = '//*[@id="ip_list"]/tbody/tr[num]/td[2]/text()'
            pattern_port = '//*[@id="ip_list"]/tbody/tr[num]/td[3]/text()'
            response = requests.get(url=url,headers=config.get_header())
            content = response.content
            selector = html.fromstring(content)
            ip = selector.xpath(pattern_ip)
            port = selector.xpath(pattern_port)
            for i in zip(ip, port):
                ip_port = i[0] + ':' + i[1]
                ip_port_list.append(ip_port)

        k = i+22
    with open(path, 'a') as f:
        f.write('\n')
        for i in ip_port_list:
            f.write(i+'\n')


def get_66ip():
    pattern_ip = '//*[@id="footer"]/div/table/tbody/tr[2]/td[1]'
    pattern_port = '//*[@id="footer"]/div/table/tbody/tr[2]/td[2]'
    urls = ['http://m.66ip.cn/areaindex_{}/1.html'.format(num) for num in range(1,35)]
    for url in urls:
        time.sleep(2)
        print(url)
        try:
            content = requests.get(url=url, headers=config.get_header()).content
            print(content.decode())
            selector = html.fromstring(content.decode())
            ips = selector.xpath(pattern_ip)
            ports = selector.xpath(pattern_port)
            print(ips,ports)
            ip_ports = [ip + ":" + port for ip, port in zip(ips, ports)]
            print(ip_ports)
        except Exception as e:
            print('{}无法访问,{}'.format(url,e))
    print(urls)



if __name__ == '__main__':
    get_dxdlspider()
    get_kdlspider()
    # get_xicidailispinder()