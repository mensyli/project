from selenium import webdriver
import os
import time

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir",os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")

driver = webdriver.Firefox(firefox_profile=fp)
driver.get("http://pypi.python.org/pypi/selenium")
driver.find_element_by_partial_link_text("geckodriver").click()
time.sleep(5)
new_handle = driver.current_window_handle
content = driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[2]/div[1]/div[2]/ul/li[5]/a')
content.click()