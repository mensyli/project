from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.youdao.com")

driver.add_cookie({'name':'dsdsdsdsdsdsd','value':'ddsdsdsds'})


cookies = driver.get_cookies()
for cookie in cookies:
    print("%s->%s" % (cookie['name'],cookie['value']))
#print(cookie)