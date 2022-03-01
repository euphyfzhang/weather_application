# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:21:55 2018

@author: euphyfzhang
"""

import urllib
import json
from datetime import datetime

def KtoC(kelvin):
    return round(kelvin-273.15, 2)

def dtF(ms):
    return datetime.fromtimestamp(ms)

class WeatherChecker:
    def getTable(self):
        try:
            return self.table
        except Exception:
            return 'N/A'

    def getInfo(self,*items):
        try:
            if len(items) == 1:
                return self.table[items[0]]
            elif len(items) == 2:
                return self.table[items[0]][items[1]]
            elif len(items) == 3:
                return self.table[items[0]][items[1]][items[2]]
        except Exception:
            return 'N/A'
    
class WeatherCheckerCityCountry(WeatherChecker):
    
    def __init__(self, city, cntry):
        self.city = city
        self.cntry = cntry
        self.table = json.loads(urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q={0},{1}&appid=1b313b85c6052efdec5fc36ed590c1da'.format(self.city,self.cntry)).read())
    
    
class WeatherCheckerCityID(WeatherChecker):
    
    def __init__(self, cityid):
        self.cityid = cityid
        self.table = json.loads(urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id={0}&appid=1b313b85c6052efdec5fc36ed590c1da'.format(self.cityid)).read())
    

class WeatherCheckerLonLat(WeatherChecker):
    
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat
        self.table = json.loads(urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid=1b313b85c6052efdec5fc36ed590c1da'.format(self.lat,self.lon)).read())
    
 

# =============================================================================
#         if(url.getcode()==200):
#             data = url.read()
#             readResult(data)
#         else:
#             print("Cannot parse data")
# =============================================================================

def main():
    wc = WeatherCheckerCityCountry('perth','au')
    print(wc.getTable())
    print(wc.getInfo('name'))

if __name__ == '__main__':
    main()