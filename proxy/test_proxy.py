import requests
import os
from multiprocessing.dummy import Pool

basedir = os.getcwd() + '/result/'
filename = basedir + 'alive_ip.txt'

alive_ip = []

pool =Pool(20)

def test_alive(proxy):
	proxies = {'http':proxy}
	print('Now testing:{}'.format(proxies))

	try:
		r = requests.get('http://www.mmjpg.com/',proxies=proxies,timeout=30)
		r.raise_for_status()
		alive_ip.append(proxy)
	except:
		print('The proxy {} lose efficacy '.format(proxy))

def out_file(alive_ip):
	with open(filename,'a+') as f:
		for ip in alive_ip:
			f.write(ip + '\n')
		print('All outputs completed ')

def test(file):
	with open(basedir + file,'r') as f:
		lines = f.readlines()
		proxys = list(map(lambda x:x.strip(), [y for y in lines]))

		pool.map(test_alive,proxys)

	out_file(alive_ip)


if __name__ == '__main__':
	print(os.getcwd())
	test('dxdlspider.txt')
	test('kdlspider.txt')