### Administrator Change Market Hours Stock PSEUDOCODE ###

# takes place after Administrator login

    
import datetime
from msilib import OpenDatabase
import time


def setMarketHours():
    # sets time users will be able to make trades 
    # sets DAILY "open" time and "close" time
    OpenTime = time #9:00
    CloseTime = time #16:00

    # sets "Date of Week" open and close
    OpenDate = date #Monday
    CloseDate = date #Friday


    # checks if market is closed
    if MarketOpen <= current_time <= MarketClose
    return "Stock Market is Closed for the Day"
    
    
