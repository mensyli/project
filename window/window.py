from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time


# driver = webdriver.Chrome()
# driver.implicitly_wait(10)
# driver.get('http://www.baidu.com')
# search_window = driver.current_window_handle
# driver.find_element_by_link_text('登录').click()
# driver.find_element_by_link_text('立即注册').click()
# all_handlers = driver.window_handles
# time.sleep(5)
#
# for handler in all_handlers:
#     if handler != search_window:
#         driver.switch_to_window(handler)
#         print('Now register window')
#         driver.find_element_by_name('userName').send_keys('username')
#         driver.find_element_by_name('password').send_keys('password')
#         time.sleep(5)
#
#
# for handler in all_handlers:
#     if handler == search_window:
#         driver.switch_to_window(handler)
#         print('Now search window')
#         driver.find_element_by_id('TANGRAM__PSP_2__closeBtn').click()
#         driver.find_element_by_id('kw').send_keys('selenium')
#         driver.find_element_by_id('su').click()
#         time.sleep(5)

# driver.quit()

driver = webdriver.Chrome()
driver.get("http://image.baidu.com")
# driver.implicitly_wait(10)
driver.find_element_by_id("sttb").click()

for i in range(10):
    stfile = driver.find_element_by_xpath('//*[@id="uploadImg"]')
    if stfile.is_displayed():
        break
    else:
        pass
    time.sleep(1)
stfile.click()
# stfile = WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.ID,"uploadImg")))
# stfile = driver.find_element_by_xpath('//*[@id="uploadImg"]').click()
# stfile.click()


os.system("F:\\Windows\\Document\\pycharm\\open.exe")

cookies = driver.get_cookies()
print(cookies)
