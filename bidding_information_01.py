import requests as requests

requests.packages.urllib3.disable_warnings()#关闭安全警告
from selenium import webdriver
import time

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("-Referer='https://www.https://b2b.10086.cn/b2b/main/showBiao!preShowBiao.html?noticeType=list1'")
driver_path=r'D:\driver\chromedriver.exe'
driver=webdriver.Chrome(executable_path=driver_path)
url="https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=727291"
newwindow='window.open("https://baidu.com");'
driver.execute_script(newwindow)

# driver.get(url)
time.sleep(3)
print(driver.page_source)

