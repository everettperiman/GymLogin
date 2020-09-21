# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:33:47 2020

@author: evere
"""

from selenium import webdriver
import chromedriver_binary
from selenium.common.exceptions import NoSuchElementException

import json
import configparser
import time


class slotItem():
    def __init__(self,webElementObject,ID):
        self.webObj = webElementObject
        self.id = ID
        self.text = webElementObject.text
        self.time_properties = self.getSlotInformation(self.text)
        
    def getSlotInformation(self,slotText):
        old_index = 0
        outputArray = []
        for index, element in enumerate(slotText):
            if element == "\n":
                outputArray.append(slotText[old_index : index])
                old_index = index + 1
        for item in outputArray:
            if item == '':
                outputArray.remove(item)
        return outputArrays

class reserveBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.userName = ''
        self.userPass = ''
        self.url = "https://ucfrwc.org/Program/GetProducts?productTypeCV=00000000-0000-0000-0000-000000003502"
        self.retries = 5
        self.allSlots = []
        self.openSlots = []
        self.scheduleSlots = []
        #self.schedule = ""
        
    def getLoginDetails(self,address):
        config = configparser.ConfigParser()
        config.read(address)    
        self.userName = config['LOGIN']['username']
        self.userPass = config['LOGIN']['password']

    def getScheduleDetails(self,address):
        with open(address, "r") as read_file:
            self.schedule = json.load(read_file)


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
        self.allSlots.clear()
        defaultSlots = [i for i in range(0,100) if (i-1) % 3 == 0]
        defaultStrings = ["div.col-sm-6:nth-child({}) > div:nth-child(1) > div:nth-child(1)".format(i) for i in defaultSlots]
        for index, string in enumerate(defaultStrings):
            try:
                slot_Obj = self.driver.find_element_by_css_selector(string)
                self.allSlots.append(slotItem(slot_Obj, defaultSlots[index]))
            except NoSuchElementException:
                pass    
            except Exception as e:
                print(e)
                print("Bad slot" + string)

    def getOpenSlots(self):
        # Filters the results of the getSlots method to return Slots that have
        # Open reservation availability
        self.openSlots.clear()
        self.getSlots()
        for slot in self.allSlots:
            if "No Spots" not in slot.text:
                self.openSlots.append(slot)
            else:
                slot.time_properties[-1] = "0 spot(s) available"

    def getScheduleSlots(self):
        # Filters the results of the getSlots method to return Slots that have
        # Open reservation availability
        self.scheduleSlots.clear()
        self.getOpenSlots()
        if len(self.openSlots) > 0:
            for slot in self.openSlots:
                for schedule in self.schedule['Schedule']:
                   if (schedule['Day'] in slot.time_properties[0] and schedule['Time'] in slot.time_properties[1][:8]):
                       self.scheduleSlots.append(slot)

    def getHomePage(self):
        # Resets the current tab to the main selection page to create more
        # Reservations
        home_url = 'https://ucfrwc.org/Program/GetProducts'
        self.driver.get(home_url)
        
    def reserveSlot(self,slotID,test=True):
        # Takes the child(slotID) of the desired slot and finishes the 
        # Checkout process
        slotID = "div.col-sm-6:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)".format(slotID)
        self.handleElementCSS(slotID, self.retries)
        self.handleElementCSS("div.container-fluid:nth-child(6) > button:nth-child(2)", self.retries)
        self.handleElementCSS("#checkoutButton", self.retries)
        if not test:
            self.handleElementCSS("div.modal-footer:nth-child(2) > button:nth-child(2)", self.retries)
        else:
            self.handleElementCSS("div.modal-footer:nth-child(2) > button:nth-child(1)", self.retries)
            self.handleElementCSS("button.allow-navigation:nth-child(1)", self.retries)

def logFreeSlots(slotArray,name="log.txt"):
    read_time = time.ctime()
    print(read_time)
    with open(name,"a") as file:
        if len(slotArray) > 0:
            for slot in slotArray:
                file.write(read_time + ", " + slot.time_properties[0].replace(",","") + ", " + slot.time_properties[1] + ", " + slot.time_properties[2][0:2] + "\n")
        else:
            file.write(read_time + ", No Free Slots" + "\n")

        
if __name__ == "__main__":
    
    refresh_count = 0

    EasyMoney = reserveBot()
    
    loginDetails = r'C:\Users\evere\OneDrive\Desktop\login.ini'
    scheduleDetails = r'C:\Users\evere\OneDrive\Desktop\schedule.txt'
    EasyMoney.getLoginDetails(loginDetails)
    EasyMoney.getScheduleDetails(scheduleDetails)    
    
    EasyMoney.driver.get(EasyMoney.url)
    EasyMoney.nidLogin()
    EasyMoney.navPage("facilitys","pool")
    
    scheduledTimes = EasyMoney.getScheduleSlots();
    print(EasyMoney.scheduleSlots[0].time_properties[0])
    EasyMoney.reserveSlot(EasyMoney.scheduleSlots[0].id)

    
    
    
    
        


