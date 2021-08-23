#!/usr/bin/env python
# coding: utf-8

# In[4]:


# In[1]:


import pyautogui as pg
import time


# In[ ]:


#move to previous_day folder

#click on folders
pg.click(763,1064)

time.sleep(3)

#click on downloads
pg.click(111,346)

time.sleep(2)

#click on bar in downloads
pg.moveTo(1724,209)

time.sleep(1)

pg.click(1724,209)
time.sleep(1)

#type in previous_day%
pg.typewrite('previous_day', interval=0.1)
time.sleep(2)

#click on previous_close folder
pg.click(1750,231)

time.sleep(2)

#delete

pg.click(439,90)

time.sleep(2) 
