#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pyautogui as pg


# In[3]:


import time

#pg.position() gets position


# In[5]:


# #order
# 1.	Open TWS 
# 2.	Enter username and password.
# 3.	Open chrome, go to gmail, click right places, get to the email, open it, highlight the code, copy it
# 4.	Paste it, hit ok 

#takes about 65 seconds, run at 720 ish. 

#click on bottom right of screen to get to desktop
pg.click(1919,1074)
time.sleep(1)

#double click on TWS
pg.click(55,171)
pg.click(55,171)
time.sleep(30) #in case there is an update

#click on live
pg.click(900,488)

#click on username
pg.moveTo(907,537)
time.sleep(1)
pg.click(907,537)

#type login id
pg.typewrite('hoba8888', interval=0.1)


#click on password part
pg.click(874,573)
time.sleep(1)


#type password
pg.typewrite('mhkp1234', interval=0.1)

#shift it over a bit 

pg.moveTo(937,286)

time.sleep(0.5)

pg.dragTo(1279,286,2)

time.sleep(0.5)

#click login
pg.click(1278,636)
time.sleep(2)




#click on search bar
pg.click(140,1057)

#type in chrome
pg.typewrite('chrome',interval=0.1)

time.sleep(1)

#click on incognito
pg.click(776,719)

time.sleep(1)

#max it out
pg.click(1838,33)

#click on search bar
pg.click(951,62)

time.sleep(1)

#type in gmail

pg.typewrite('gmail.com\n',interval=0.1)

time.sleep(3)

#type in username and password

pg.typewrite('matthewharwit\n',interval=0.1)

time.sleep(3)

pg.typewrite('Hobajons8\n',interval=0.1)

time.sleep(10)

#click on first link

pg.click(717,328)

time.sleep(1)

#move TWS prompt to the side

pg.moveTo(943,427)

time.sleep(0.5)

pg.dragTo(1515,427,2)

time.sleep(1)

#click back on gmail
pg.click(897,326)




#grab code

pg.moveTo(672,420)

time.sleep(1)

pg.dragTo(737,421,0.6) 

time.sleep(1)

pg.hotkey('ctrl', 'c')

time.sleep(1)

#click back on TWS

pg.click(1392,465)

time.sleep(1)

pg.hotkey('ctrl', 'v')

#enter

time.sleep(1)

#click ok
pg.click(1428,597)



