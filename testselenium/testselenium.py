# _*_coding:utf-8_*_

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


browser = webdriver.Edge()
browser.get('http://www.baidu.com')
print('现在将浏览器最大化')
browser.maximize_window()
text = browser.find_element_by_name('tj_trnews').text
print(text)
time.sleep(1)

browser.find_element_by_id('kw').send_keys('selenium')
print(browser.find_element_by_id('kw').get_attribute('type'))
print(browser.find_element_by_id('kw').size)
browser.find_element_by_id('su').click()
time.sleep(3)


print('现在我将浏览器设置为800x480')
browser.set_window_size(800, 480)
browser.get('http://m.mail.10086.cn')
time.sleep(2)

print('现在我们回到刚才的页面')
browser.maximize_window()
browser.back()
time.sleep(2)

print('现在我们将回到之前的页面')
browser.forward()
time.sleep(2)

browser.get('http://www.yangyanxing.com')
browser.find_element_by_xpath(".//*[@id='search-form-wrap']/form/input[1]").click()
browser.find_element_by_xpath(".//div[2]/div[2]/div/input").send_keys('python')
browser.find_element_by_xpath(".//div[2]/div[2]/div[2]/div/section[1]/div[1]").click()
time.sleep(2)


print('以下将以登录人人网来进行上面的综合应用')
browser.get('http://www.renren.com/SysHome.do')
browser.find_element_by_id('email').clear()
browser.find_element_by_id('email').send_keys('limg2007gmil@163.com')
time.sleep(1)
browser.find_element_by_id('email').send_keys(Keys.BACK_SPACE)
time.sleep(1)
browser.find_element_by_id('email').send_keys(Keys.CONTROL, 'a')
time.sleep(1)
browser.find_element_by_id('email').send_keys(Keys.CONTROL, 'x')
time.sleep(1)
browser.find_element_by_id('email').send_keys(Keys.CONTROL, 'v')
time.sleep(1)
browser.find_element_by_id('email').send_keys('m')
browser.find_element_by_id('password').clear()
browser.find_element_by_id('password').send_keys('Qq!@#$%^&*()')
browser.find_element_by_id('autoLogin').click()
browser.find_element_by_id('login').click()