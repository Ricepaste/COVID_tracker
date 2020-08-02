# get covid-19 confirmed cases

from selenium import webdriver  #安裝指令 pip install selenium
import time

user = 1
if user == 0:
    path = r'D:\Users\Administrator\Desktop\asfsaf\Python\collect_COVID-19\chromedriver.exe'
else:
    path = r'D:\實驗爬蟲\chromedriver.exe'

class Get_virus():
    def __init__(self): # initialization
        self.driver = webdriver.Chrome(path)   #從webdriver.Chrome(path) 把driver路徑放入該函數
        self.driver.get('https://www.worldometers.info/coronavirus/')

        try:
            time.sleep(5) # wait for 5 sec to load the page
            self.get_data()
        except:
            self.driver.quit()

    def get_data(self):
        table = self.driver.find_element_by_xpath('//*[@id="nav-tabContent"]')
        tbody = table.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
        con_ids = tbody.find_element_by_xpath("//tr[contains(., 'Taiwan')]")
        con = con_ids.find_elements_by_tag_name('td')

        con_datas = []

        for data in range(1, len(con)-1):
            # print(data, con[data].text)
            con_datas.append(con[data].text)

        print('found datas: ', con_datas)

Get_virus()
