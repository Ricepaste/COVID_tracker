from selenium import webdriver  #安裝指令 pip install selenium
import time

path = r'D:\Users\Administrator\Desktop\asfsaf\Python\collect_COVID-19\chromedriver.exe'

class Get_virus():
    def __init__(self): # initialization
        self.driver = webdriver.Chrome(path)   #從webdriver.Chrome(path) 把driver路徑放入該函數
        self.driver.get('https://www.worldometers.info/coronavirus/')

        try:
            time.sleep(5) # wait for 5 sec to load the page
            self.get_data()
        except:
            print('broken')
            self.driver.quit()

            Get_virus()
            

    def get_data(self):
        table = self.driver.find_element_by_xpath('//*[@id="nav-tabContent"]')
        tbody = table.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
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

Get_virus()