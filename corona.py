# get covid-19 confirmed cases

from selenium import webdriver  #安裝指令 pip install selenium
import time

user = 1
if user == 0:
    path = r'D:\Users\Administrator\Desktop\asfsaf\Python\collect_COVID-19\chromedriver.exe'
else:
    path = r'D:\實驗爬蟲\chromedriver.exe'

class Get_virus():
    def __init__(self, mode=None): # initialization
        self.driver = webdriver.Chrome(path)   #從webdriver.Chrome(path) 把driver路徑放入該函數
        self.driver.get('https://www.worldometers.info/coronavirus/')

        try:
            time.sleep(5) # wait for 5 sec to load the page
            if mode == 'p' or 'partial':
                self.partial_get_data()
            else:
                self.get_data()
        except:
            print('broken')
            self.driver.quit()

    def get_data(self):
        table = self.driver.find_element_by_xpath('//*[@id="nav-tabContent"]')
        tbody = table.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
        # con_ids = tbody.find_element_by_xpath("//tr[contains(., 'Taiwan')]")
        # con = con_ids.find_elements_by_tag_name('td')
        con_ids = tbody.find_elements_by_xpath('tr')

        con_datas = {}
        temp_datas = []

        empty = False

        for x in con_ids: # chek all ids
            con = x.find_elements_by_tag_name('td') 

            empty = False
            for data in range(2, len(con)-1):
                if con[1].text == '': # check if it is empty
                    print('empty')
                    empty = True

                    break

                temp_datas.append(con[data].text)

            if not empty: # if the data is not empty, store it
                print('get: ', con[1].text)           

                con_datas[con[1].text] = temp_datas # con[1].text is country name

            temp_datas = []

        print('found datas: ', con_datas)

        print(con_datas['Taiwan'])
    
    def partial_get_data(self):
        temp_datas = []
        table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
        country_table = table.find_element_by_xpath("//tr[contains(., 'Taiwan')]")
        target = country_table.find_elements_by_tag_name('td')
        for i in target:
            if i.text != '':
                temp_datas.append(i.text)
        print(temp_datas)

Get_virus('p')