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
    
    def nidLogin(self):
        self.driver.find_element_by_id('loginLink').click() #Log In Button
        self.handleElementCSS(".btn-soundcloud", self.retries) # UCF NID Option
        self.driver.find_element_by_css_selector("#username").send_keys(self.userName) # Input Username
        self.driver.find_element_by_css_selector("#password").send_keys(self.userPass) # Input Password
        self.driver.find_element_by_css_selector(".btn").click() # Click Sign on Button
        self.handleElementCSS("#gdpr-cookie-accept", self.retries) # Accept cookies button to avoid future errors


    def navPage(self,classif = None, option=None):
        # Xpath Keys for all of the Classification and subcategories
        # Sets Parent and Child for all of these and then navigates to the
        # Desired path
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
        # Handle pages loading to slow or something temporarily covering 
        # The desired option
        i = 0
        while(i < attempts):
            try:
                self.driver.find_element_by_xpath(xpath).click()
                break
            except:
                time.sleep(sleepTime)
                i += 1
                
    def handleElementCSS(self,cssSelector,attempts,sleepTime = 1):
        # Handle pages loading to slow or something temporarily covering 
        # The desired option
        i = 0
        while(i < attempts):
            try:
                self.driver.find_element_by_css_selector(cssSelector).click()
                break
            except:
                time.sleep(sleepTime)
                i += 1        
        
    def getSlots(self):
        # All of the slots are layed out as child(number) with these4 numnbers
        # Starting at 1 and are sums of n + 3 and there is no max number found
        # As of yet for these numbers
        # This section determines the max # of slots and returns an array of
        # WebElement objects
        goodSlots = []
        defaultSlots = [i for i in range(0,100) if (i-1) % 3 == 0]
        defaultStrings = ["div.col-sm-6:nth-child({}) > div:nth-child(1) > div:nth-child(1)".format(i) for i in defaultSlots]
        for index, string in enumerate(defaultStrings):
            try:
                goodSlots.append([self.driver.find_element_by_css_selector(string), defaultSlots[index]])        
            except NoSuchElementException:
                pass    
            except Exception as e:
                print(e)
                print("Bad slot" + string)
        
        return goodSlots;
    
    def getOpenSlots(self):
        # Filters the results of the getSlots method to return Slots that have
        # Open reservation availability
        slotElements = self.getSlots()
        open_slots = []
        for slot in slotElements:
            if "No Spots" not in slot[0].text:
                open_slots.append(slot)
        return open_slots;
                         
    def siteHomepage(self):
        # Resets the current tab to the main selection page to create more
        # Reservations
        home_url = 'https://ucfrwc.org/Program/GetProducts'
        self.driver.get(home_url)
        
    def reserveSlot(self,slotID,test=True):
        # Takes the child(slotID) of the desired slot and finishes the 
        # Checkout process
        slotID = "div.col-sm-6:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)".format(slotID)
        self.driver.find_element_by_css_selector(slotID).click()
        self.driver.find_element_by_css_selector("div.container-fluid:nth-child(6) > button:nth-child(2)").click()
        self.driver.find_element_by_css_selector("#checkoutButton").click()
        if not test:
            self.driver.find_element_by_css_selector("div.modal-footer:nth-child(2) > button:nth-child(2)").click()

        
if __name__ == "__main__":
    
    refresh_count = 0
    config = configparser.ConfigParser()
    config.read(r'C:\Users\evere\OneDrive\Desktop\login.ini')
    
    EasyMoney = reserveBot(config['LOGIN']['username'], config['LOGIN']['password'])
    EasyMoney.schedule = config['SCHEDULE']['options']
    EasyMoney.driver.get(EasyMoney.url)
    EasyMoney.nidLogin()
    EasyMoney.navPage("facilitys","gym")
    
    while True:
        pink = EasyMoney.getOpenSlots()
        if len(pink) > 0:
            print(refresh_count)
            EasyMoney.reserveSlot(pink[0][-1])
                
            break
        refresh_count += 1
        time.sleep(5)
        EasyMoney.driver.refresh()

    
    
    
    
        


