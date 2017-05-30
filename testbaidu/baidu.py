# coding=utf-8

from selenium import webdriver
import time

driver = webdriver.Edge()
driver.get('http://www.baidu.com')
driver.find_element_by_id('kw').send_keys('selemium2')
driver.find_element_by_id('su').click()
time.sleep(10)
driver.quit()