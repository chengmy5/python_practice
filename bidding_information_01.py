from selenium import webdriver
import time

driver_path=r'D:\driver\IEDriverServer.exe'
driver=webdriver.Ie(executable_path=driver_path)
url="https://b2b.10086.cn/b2b/main/showBiao!preShowBiao.html?noticeType=list1"
driver.get(url)
time.sleep(3)
content=driver.page_source
driver.quit()
print(content)
