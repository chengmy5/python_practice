from selenium import webdriver
import time

# driver_path=r'D:\driver\IEDriverServer.exe'
# driver=webdriver.Ie(executable_path=driver_path)
driver_path=r'D:\driver\chromedriver.exe'
driver=webdriver.Chrome(executable_path=driver_path)
url="http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id=402882ac769a385f0176b1a737b74657"
driver.get(url)
# time.sleep(5)
# startTime=driver.find_element_by_name('noticeBean.startDate')
# startTime.send_keys('2021-01-01')
# endTime=driver.find_element_by_name('noticeBean.endDate')
# endTime.send_keys('2021-01-05')
# search=driver.find_element_by_id('search')
# search.click()
# time.sleep(700)
content=driver.page_source
print(content)
