# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:33:47 2020

@author: evere
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException

import configparser
import time


class reserveBot():
    def __init__(self,uName,uPass):
        webdriver_path = r'C:\Users\evere\anaconda3\geckodriver.exe'
        self.driver = webdriver.Firefox(executable_path=webdriver_path)
        self.userName = uName
        self.userPass = uPass
        self.url = "https://ucfrwc.org/Program/GetProducts?productTypeCV=00000000-0000-0000-0000-000000003502"
        self.wait = WebDriverWait(self.driver, 10)
        self.retries = 5
        
    def getGoodSlots(self):
        driver = self.driver
        url = self.url       
        css_list = [1,4,7,10,13,16,19,25]
        time_slots = []
        good_time_slots = []               
        self.nidLogin()
        self.navPool()
        for css_item in css_list:
            try:
                item_string = "#mainContent > div:nth-child(2) > div.list-group > div:nth-child({}) > div > div ".format(css_item)
                item = driver.find_element_by_css_selector(item_string)
                time_slots.append([item,css_item])
            except:
                print("Bad slot" + str(css_item))
        
        for x in time_slots:
            y = x[0].text
            if "available" in y:
                good_time_slots.append(x)
            
        if (len(good_time_slots) > 0):      
            driver.find_element_by_css_selector("#mainContent > div:nth-child(2) > div.list-group > div:nth-child({}) > div > div > div > button".format(good_time_slots[0][1])).click()
            driver.find_element_by_css_selector("#checkoutButton").click()
        
        return 0;
    
    def nidLogin(self):
        self.driver.find_element_by_id('loginLink').click()
        self.handleElementCSS(".btn-soundcloud", self.retries)
        self.driver.find_element_by_css_selector("#username").send_keys(self.userName)
        self.driver.find_element_by_css_selector("#password").send_keys(self.userPass)
        self.driver.find_element_by_css_selector(".btn").click()
        self.handleElementCSS("#gdpr-cookie-accept", self.retries)


    def navPage(self,classif = None, option=None):
        if classif == 'facilitys':
            xpath_parent = '//*[@id="6075734c-eb15-4687-9453-59115958bbc0"]'
            if option == 'pool':
                xpath_child = '//*[@id="list-group"]/div[1]/div/div[2]'
            elif option == 'gym':
                xpath_child = '//*[@id="list-group"]/div[2]/div/div[2]'
        
        elif classif == 'fitness':
            xpath_parent = '//*[@id="00000000-0000-0000-0000-000000026002"]'
        
        elif classif == 'instruction':
            xpath_parent = '//*[@id="00000000-0000-0000-0000-000000026001"]'
        
        elif classif == 'outdoor':
            xpath_parent = '//*[@id="7e94c055-5e69-4046-8e3d-96909ff99f22"]'

        self.handleElementXpath(xpath_parent, self.retries)
        self.handleElementXpath(xpath_child, self.retries)

    
    def handleElementXpath(self,xpath,attempts,sleepTime = 1):
        i = 0
        while(i < attempts):
            try:
                self.driver.find_element_by_xpath(xpath).click()
                break
            except:
                time.sleep(sleepTime)
                i += 1
                
    def handleElementCSS(self,cssSelector,attempts,sleepTime = 1):
        i = 0
        while(i < attempts):
            try:
                self.driver.find_element_by_css_selector(cssSelector).click()
                break
            except:
                time.sleep(sleepTime)
                i += 1        
        
    def getSlots(self):
        goodSlots = []
        defaultSlots = [i for i in range(0,100) if (i-1) % 3 == 0]
        defaultStrings = ["div.col-sm-6:nth-child({}) > div:nth-child(1) > div:nth-child(1)".format(i) for i in defaultSlots]
        
        for string in defaultStrings:
            try:
                goodSlots.append(self.driver.find_element_by_css_selector(string))
                
            except NoSuchElementException:
                pass
            
            except Exception as e:
                print(e)
                print("Bad slot" + string)
        
        return goodSlots;
    
    def getOpenSlots(self):
        slotElements = self.getSlots()
        open_slots = []
        for slot in slotElements:
            if "No Spots" not in slot.text:
                open_slots.append(slot)
        return open_slots;
                
    def siteHomepage(self):
        home_url = 'https://ucfrwc.org/Program/GetProducts'
        self.driver.get(home_url)
        
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(r'C:\Users\evere\OneDrive\Desktop\login.ini')
    
    EasyMoney = reserveBot(config['LOGIN']['username'], config['LOGIN']['password'])
    
    EasyMoney.driver.get(EasyMoney.url)
    EasyMoney.nidLogin()
    EasyMoney.navPage("facilitys","gym")
    pink = EasyMoney.getOpenSlots()
    for i in pink:
        print(i.text)

    """
    EasyMoney.siteReset()
    EasyMoney.navPage("facilitys","pool")
    EasyMoney.siteReset()
    EasyMoney.driver.close()
    """
    
    
    
    
        


