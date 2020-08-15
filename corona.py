# get covid-19 confirmed cases
'''
File "/home/pi/.local/lib/python3.7/site-packages/firebase/__init__.py", line 14, in <module>
    import python_jwt as jwt
ModuleNotFoundError: No module named 'python_jwt'
'''
'''
pip install python_jwt
pip install gcloud
pip install sseclient
pip install pycrypto
pip install requests-toolbelt
'''
from selenium import webdriver  # pip install selenium
import time
from firebase import firebase # pip install firebase
import smtplib 
from email.mime.text import MIMEText

user = 1
if user == 0:
    path = r'D:\Users\Administrator\Desktop\asfsaf\Python\collect_COVID-19\chromedriver.exe'
else:
    path = r'/usr/lib/chromium-browser/chromedriver'

class Get_virus():
    def __init__(self, mode=None): # initialization
        self.driver = webdriver.Chrome(path)   
        #from webdriver.Chrome(path) put driver's path into this fuction
        self.driver.get('https://www.worldometers.info/coronavirus/')

        # try:
        #     time.sleep(5) # wait for 5 sec to load the page
        #     if mode == 'p' or 'partial':
        #         self.partial_get_data()
        #     else:
        #         self.get_data()
        # except:
        #     print('broken')
        #     self.driver.quit()

        
        time.sleep(7) # wait for 5 sec to load the page
        if mode == 'p' or 'partial':
            self.partial_get_data()
        else:
            self.get_data()

    def ConvertToInt(self, data): #testing
        
        count = 0
        for x in range(len(data)):
            # if 'Total:' in data[x]:
            #     data[x] = data[x].replace('Total:', name[count])
            #     count += 1
            if ',' in data[x] or '+' in data[x]:
                data[x] = data[x].replace(',', '')
                data[x] = data[x].replace('+', '')
                data[x] = int(data[x])
            elif data[x] == '': 
                data[x] = 0
            elif data[x].isdigit():
                data[x] = int(data[x])
            elif '.' in data[x]:
                data[x] = float(data[x])
        return data

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
            '''
            if i.text != '':
                temp_datas.append(i.text)
            '''
            temp_datas.append(i.text)
        print(temp_datas)
        temp_datas = self.ConvertToInt(temp_datas)

        corona_data = {'data': temp_datas[2:]}
        db_url = 'https://corona-tracker-c57fc.firebaseio.com'
        fdb = firebase.FirebaseApplication(db_url, None)
        fdb.delete(temp_datas[1], None)
        fdb.post(temp_datas[1], corona_data)
        
        self.notificate(temp_datas)

    def notificate(self, data):
        '''Email'''         
        title = [
            'Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 
            'Active Cases', 'Serious, Critical', 'Tot Cases/1M pop', 'Deaths/1M pop', 'Total tests', 'Tests/1M pop',
            'population'
            ]
        count = 0

        notice = 1  #testing send email  if notice = 1 it will send email to you
        if notice == 1:  
            print('Has opened the fuction of sending email')
            
            send = smtplib.SMTP('smtp.gmail.com', 587) 
            send.ehlo()       
            send.starttls()      
            send.login('b35251103@gmail.com', 'bearchildis8787' )

            texting = ''
            data.pop()
            for i in data[1:14]:
                if count < len(title):
                    texting += title[count] + ': ' + str(i) + '\n'
                    count += 1
                else:
                    texting += '?:' + ': ' + str(i) + '\n'
            print(texting)

            msg = MIMEText(texting, 'plain', 'utf-8')  
            msg['Subject'] = 'message'  
            msg['From'] = 'where are coronavirus'    
            msg['To'] = 'Kevin'   

            state = True # False: send to Kevin True: send to everyone
            if state:
                catch = ['b35251103@gmail.com','a8829037@gmail.com', 'n048685739@gmail.com']
            else:
                catch = ['a8829037@gmail.com']
            sent = send.sendmail('b35251103@gmail.com', catch, msg.as_string())       
            if sent == {}:
                print('datas have been sent')
            send.quit()  

Get_virus('p')
