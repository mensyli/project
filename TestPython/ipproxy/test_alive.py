import requests
import setting
import config
from multiprocessing.dummy import Pool as ThreadPool



alive_ip = []
path = setting.save_ip
pool = ThreadPool()
pool = ThreadPool(20)
def test_alive(proxy):
    proxies = {'http':proxy}
    print('正在测试{}'.format(proxies))
    try:
        r = requests.get('http://www.mmjpg.com', headers=config.get_header(),proxies=proxies)
        print(proxies)
        if r.status_code == 200:
            print('该代理：{}成功存活'.format(proxy))
            alive_ip.append(proxy)
    except:
        print('该代理{}失效！'.format(proxies))


def Out_file(alivename=""):

    with open(path + alivename, 'a') as f:
        for ip in alive_ip:
            ip = ip.strip()
            if ip != "":
                f.write(ip+'\n')
        print('所有存活ip都已经写入文件！')


def test(filename='blank.txt'):

    with open(path + filename, 'r') as f:
        lines = f.readlines()
        proxys = list(map(lambda x: x.strip(), [y for y in lines]))

        # 一行代码解决多线程！
        pool.map(test_alive, proxys)



if __name__ == '__main__':
    test('a1.txt')
    test('a2.txt')
    Out_file('alive_ip.txt')