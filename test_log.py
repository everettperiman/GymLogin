# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 11:37:04 2020

@author: evere
"""
from reserve import *

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
    
    LogBot = logBot("pool.txt")

    while(True):
        Bot.refreshPage()
        Bot.getSlots()
        LogBot.storeReading(Bot.allSlots)
        time.sleep(60)
    