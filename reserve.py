# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:33:47 2020

@author: evere
"""

from selenium import webdriver
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import json
import configparser
import time
import datetime as dt

class userDetails():
    def init(self):
        self.username
        self.password
        self.schedule
    
    def get_login(self, loginDir):
        config = configparser.ConfigParser()
        config.read(loginDir)    
        self.username = config['LOGIN']['username']
        self.password = config['LOGIN']['password']
    
    def get_schedule(self, schDir):
        with open(schDir, "r") as read_file:
            self.schedule = json.load(read_file)
    
    def print_schedule(self):
        for i in self.schedule['Schedule']:
            print("Time " + i["Day"] + " @ " + i["Time"])
    
    def print_details(self):
        print("Username: " + self.username)
        print("Password: " + self.password)
        self.print_schedule()

class slotItem():
    def __init__(self,webObject,_id):
        self.object = webObject
        self.id = _id
        self.text = webObject.text
        self.time_properties = self.getSlotInformation(self.text)
        self.spaces = self.getSlotSpaces(self.time_properties)
        self.dateTime = self.getSlotDatetime(self.time_properties)
        
    def getSlotInformation(self,slotText):
        stringA = ""
        slotInfoArr = []
        old_index = 0
        for index, char in enumerate(slotText):
            if char == "\n":
                stringA = slotText[old_index : index]
                old_index = index + 1
                if len(stringA) > 0:
                    slotInfoArr.append(stringA)
        return slotInfoArr
    
    def getSlotDatetime(self, slotInfoArray):
        slotInfo = slotInfoArray[0] + " " + slotInfoArray[1]
        for index, char in enumerate(slotInfo):
            if char == "-":
                stop_index = index
                
        green = dt.datetime.strptime(slotInfo[:stop_index], "%A, %B %d, %Y %I:%M %p ")
        return green
        
    def getSlotSpaces(self, slotInfoArray):
        stop_index = 0
        retSpaces = 0
        for char in slotInfoArray[-1]:
            stop_index += 1 
            if char == " ":
                if (slotInfoArray[-1][:stop_index - 1] != "No"):
                    retSpaces = int(slotInfoArray[-1][:stop_index - 1])
                else:
                    retSpaces = 0
                break
        return retSpaces
       
class logBot():
    def __init__(self, logFile):
        self.logFile = logFile
    
    def storeReading(self, slots):
        curDateTime = dt.datetime.now().isoformat()
        with open(self.logFile, 'a', newline = '') as log:
            for slot in slots:
                log.write(curDateTime + " ")
                log.write(slot.dateTime.isoformat())
                log.write(" {} \n".format(slot.spaces))
            print("Log Success")
   
    def getReadings(self):
        dataLogArray = []
        with open(self.logFile, 'r', newline = '') as log:
            dataLog = log.readlines()
        
        dataLogArray = [(dt.datetime.fromisoformat(line[:26]), 
                         dt.datetime.fromisoformat(line[27:46]), 
                         int(line[-3:-2])) for line in dataLog]
        self.dataLogArray = dataLogArray
        
    def displayPlot(self):
        try:
            dataArray = self.dataLogArray
        except:
            print("No data to display!")
            print("Call getReadings first!")
            return
            
        seriesArray = []
        for i in dataArray:
            if i[1] not in seriesArray:
                seriesArray.append(i[1])
        for i in seriesArray:
            x_slots = []
            y_slots = []
            for j in dataArray:
                if i == j[1]:
                    x_slots.append(j[0])
                    y_slots.append(j[-1])
            plt.plot(x_slots, y_slots)

class reserveBot():
    def __init__(self, printFlag = True):
        chrome_options = Options()  
        chrome_options.add_argument("--headless") 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.url = "https://ucfrwc.org/Program/GetProducts?productTypeCV=00000000-0000-0000-0000-000000003502"
        self.home_url = 'https://ucfrwc.org/Program/GetProducts'
        self.retries = 5
        self.allSlots = []
        self.openSlots = []
        self.scheduleSlots = []
        self.printFlag = printFlag
        
    def getPage(self, url):
        self.driver.get(url)
        
    def refreshPage(self):
        self.driver.refresh()
        
    def printSlots(self,slotList):
        print("\nPrinting Slot List!\n")
        if len(slotList) > 0:
            for slot in slotList:
                print(str(slot.spaces) + " " + slot.time_properties[0] + " " + slot.time_properties[1])
        else:
            print("No Slots in list")
            
        print("")

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
    
    def nidLogin(self, username, password):
        self.driver.find_element_by_id('loginLink').click() #Log In Button
        self.handleElementCSS(".btn-soundcloud", self.retries) # UCF NID Option
        self.driver.find_element_by_css_selector("#username").send_keys(username) # Input Username
        self.driver.find_element_by_css_selector("#password").send_keys(password) # Input Password
        self.driver.find_element_by_css_selector(".btn").click() # Click Sign on Button
        self.handleElementCSS("#gdpr-cookie-accept", self.retries) # Accept cookies button to avoid future errors
        if (self.printFlag):
            print("Login Success!")

    def navFacilities(self,classif = None, option=None):
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
        
        if (self.printFlag):
            print("Navigate Success!")     
        
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
            if (slot.spaces > 0):
                self.openSlots.append(slot)

    def getScheduleSlots(self, user_schedule):
        # Filters the results of the getSlots method to return Slots that have
        # Open reservation availability
        self.scheduleSlots.clear()
        self.getOpenSlots()
        if len(self.openSlots) > 0:
            for slot in self.openSlots:
                for schedule in user_schedule['Schedule']:
                   if (schedule['Day'] in slot.time_properties[0] and schedule['Time'] in slot.time_properties[1][:8]):
                       self.scheduleSlots.append(slot)
        
    def reserveNextSlot(self,scheduleSlots,test=True):
        # Takes the child(slotID) of the desired slot and finishes the 
        # Checkout process
        if len(scheduleSlots) > 0:
            slot_id = scheduleSlots[0]
            slotID = "div.col-sm-6:nth-child({}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)".format(slot_id)
            self.handleElementCSS(slotID, self.retries)
            self.handleElementCSS("div.container-fluid:nth-child(6) > button:nth-child(2)", self.retries)
            self.handleElementCSS("#checkoutButton", self.retries)
            if not test:
                self.handleElementCSS("div.modal-footer:nth-child(2) > button:nth-child(2)", self.retries)
                if (self.printFlag):
                    print("Reservation Success!")
            else:
                self.handleElementCSS("div.modal-footer:nth-child(2) > button:nth-child(1)", self.retries)
                self.handleElementCSS("button.allow-navigation:nth-child(1)", self.retries)
                if (self.printFlag):
                    print("Test Success!")      
        else:
            print("No Slots to Reserve")
        
if __name__ == "__main__":
    login_dir = r'C:\Users\evere\OneDrive\Desktop\login.ini'
    schedule_dir = r'C:\Users\evere\OneDrive\Desktop\schedule.txt'
    Everett = userDetails();
    Everett.get_login(login_dir);
    Everett.get_schedule(schedule_dir);
    
    Bot = reserveBot();
    Bot.getPage(Bot.url)
    Bot.nidLogin(Everett.username, Everett.password)
    Bot.navFacilities("facilitys","pool")
    Bot.getScheduleSlots(Everett.schedule)
    Bot.printSlots(Bot.allSlots)
    Bot.printSlots(Bot.scheduleSlots)
    
    #Bot.reserveNextSlot(Bot.scheduleSlots)
    
    LogItDown = logBot('pool.txt')
    LogItDown.storeReading(Bot.allSlots)

    
    
    
    
    
    
    
    
    
    
    