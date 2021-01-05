from selenium import webdriver
import time
driver_path=r'D:\driver\chromedriver.exe'
# driver_path=r'D:\driver\IEDriverServer.exe'
# driver_path=r'D:\driver\msedgedriver.exe'
driver=webdriver.Chrome(executable_path=driver_path)
# driver=webdriver.Ie(executable_path=driver_path)
# driver=webdriver.Edge(executable_path=driver_path)
url="https://b2b.10086.cn/b2b/main/showBiao!preShowBiao.html?noticeType=list1"
driver.get(url)
time.sleep(3)
content=driver.page_source
# next=driver.find_elements_by_css_selector('#pageid2 > table > tbody > tr > td')
# next.click()
# driver.close()
print(content)
# print(next)