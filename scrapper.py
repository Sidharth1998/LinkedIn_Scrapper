# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 19:14:07 2019

@author: Sakshu
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import xlsxwriter

class Linkedin():
    
    def getData(self):
        driver = webdriver.Firefox(executable_path= 'geckodriver.exe')
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys('')
        driver.find_element_by_id('password').send_keys('')
        driver.find_element_by_xpath("//*[@type='submit']").click()

           
        global data
        data = []


        profile_url= "https://www.linkedin.com/in/archit-gupta-806955133/"
        driver.get(profile_url)

        # #********** Profile Details **************#
        page = BeautifulSoup(driver.page_source,'lxml')
        try:
            cover = page.find('img', attrs = {'class':'profile-background-image__image relative full-width full-height'})['src']
        except:
            cover = 'None'

        try:
            profile = page.find("img", attrs = {
                'class':'lazy-image pv-top-card-section__photo presence-entity__image EntityPhoto-circle-9 loaded'})['src']
            
        except:
            profile = "None"

        try:
            title = str(page.find("li", attrs = {'class':'inline t-24 t-black t-normal break-words'}).text).strip()
        except:
            title = 'None'
        try:
            heading = str(page.find('h2', attrs = {'class':'mt1 t-18 t-black t-normal'}).text).strip()
        except:
            heading = 'None'
        try:
            loc = str(page.find('li', attrs = {'class':'t-16 t-black t-normal inline-block'}).text).strip()
        except:
            heading = 'None'


        #*******  Contact Information **********#
        time.sleep(2)
        driver.get(profile_url + 'detail/contact-info/')

        info = BeautifulSoup(driver.page_source, 'lxml')
        details = info.findAll('section',attrs = {'class':'pv-contact-info__contact-type'})
        try:
            websites = details[1].findAll('a')
            for website in websites:
                website = website['href']
                
        except:
            website = 'None'
        try:
            phone = details[2].find('span').text
        except:
            phone = 'None'
        try:
            email = str(details[3].find('a').text).strip()
        except:
            email = 'None'
        try:
            connected = str(details[-1].find('span').text).strip()
        except:
            connected = 'None'

        
        data.append({'profile_url':profile_url,'cover':cover,'profile':profile,'title':title,'heading':heading,'loc':loc,'website':website,'phone':phone,'email':email,'connected':connected,})
        print("!!!!!! Data scrapped !!!!!!")
        
        print(data)
        driver.quit()
        
    def writeData(self):
        
        workbook = xlsxwriter.Workbook("linkedin-search-data.xlsx")
        worksheet = workbook.add_worksheet('data')
        bold = workbook.add_format({'bold': True})
        worksheet.write(0,0,'profile_url',bold)
        worksheet.write(0,1,'Name',bold)
        worksheet.write(0,2,'cover',bold)
        worksheet.write(0,3,'profile image',bold)
        worksheet.write(0,4,'heading',bold)
        worksheet.write(0,5,'location',bold)
        worksheet.write(0,6,'website',bold)
        worksheet.write(0,7,'phone',bold)
        worksheet.write(0,8,'email',bold)
        worksheet.write(0,9,'connected',bold)
        
        for i in range(1,len(data)+1):
            try:
                worksheet.write(i,0,data[0]['profile_url'])
            except:
                pass
            try:
                worksheet.write(i,1,data[0]['title'])
            except:
                pass
            try:
                worksheet.write(i,2,data[0]['cover'])
            except:
                pass
            try:
                worksheet.write(i,3,data[0]['profile'])
            except:
                pass
            try:
                worksheet.write(i,4,data[0]['heading'])
            except:
                pass
            try:
                worksheet.write(i,5,data[0]['loc'])
            except:
                pass
            try:
                worksheet.write(i,6,data[0]['website'])
            except:
                pass
            try:
                worksheet.write(i,7,data[0]['phone'])
            except:
                pass
            try:
                worksheet.write(i,8,data[0]['email'])
            except:
                pass
            try:
                worksheet.write(i,9,data[0]['connected'])
            except:
                pass
            
        workbook.close()

    def start(self):
        self.getData()
        self.writeData()
if __name__ == "__main__":
    obJH = Linkedin()
    obJH.start()