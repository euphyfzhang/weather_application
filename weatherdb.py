# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:41:06 2019

@author: yf2zhang
"""

import pyodbc

conn = pyodbc.connect('DSN=EUPYODBC')

cursor = conn.cursor()
##cursor.execute("select * from DBO.DIM_COUNTRYTABLE;")

##for row in cursor:
   ## print(f'row = {row}')
    
cursor.execute("INSERT INTO DBO.DIM_COUNTRYTABLE VALUES (345,'MENLO PARK', 'US', 'UNITED STATES', 345.34);")
conn.commit()

