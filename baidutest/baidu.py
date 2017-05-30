from selenium import webdriver
import time


driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
# driver.set_window_size(1920,1080)
# driver.find_element_by_id("kw").send_keys("selenuim")
# driver.find_element_by_id('su').click()

time.sleep(5)

js = "var content = document.getElementById('kw');content.value = 'selenuim';document.getElementById('su').click()"

driver.execute_script(js)
time.sleep(3)