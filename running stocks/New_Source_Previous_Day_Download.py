#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pyautogui as pg
import time


# In[22]:


pg.position()


# In[ ]:





# In[11]:


#click on search bar
pg.click(414,1048)
time.sleep(2)

#type in chrome
pg.typewrite('chrome', interval=0.1)
time.sleep(1)

#click chrome
pg.click(342,451)
time.sleep(1)

#max out the page
pg.click(1843,39)
time.sleep(1)

pg.click(835,29)
time.sleep(1)

#click on search bar
pg.click(717,66)
time.sleep(1)

#type in nasdaq url 
pg.typewrite('https://www.eoddata.com/download.aspx\n', interval=0.1)

time.sleep(5)

#click on home
pg.click(377,183)
time.sleep(2)

#click on download
pg.moveTo(506,223)
time.sleep(1)
pg.click(506,223)
time.sleep(2)

#click on exchange drag down and select OTC
pg.click(716,387)
time.sleep(1)

pg.click(625,752)
pg.click(625,752)
time.sleep(1)

#click download
pg.moveTo(550,644)
time.sleep(1)
pg.click(550,644)

time.sleep(5)







#same thing, but for US Equities CSV
pg.click(603,350)
time.sleep(1)

#click download
pg.moveTo(550,644)
time.sleep(1)
pg.click(550,644)
time.sleep(5)





# In[24]:


#move to previous_day folder

#click on folders
pg.click(763,1064)

time.sleep(3)

#click on downloads
pg.click(111,346)

time.sleep(2)

#click and copy the two csv files
pg.moveTo(532,300)
pg.dragTo(532,336,2)

pg.hotkey('ctrl', 'c')

time.sleep(2)

#type in previous_day to search bar
pg.click(214,1058)
time.sleep(1)

#type in previous_day
pg.typewrite('previous_day')
time.sleep(2)

#click on previous day folder
pg.click(234,447)
time.sleep(1)

#Delete previous day

pg.hotkey('ctrl', 'a')

time.sleep(0.5)

pg.click(441,88)

time.sleep(2)

pg.hotkey('ctrl', 'v')
time.sleep(1)



# In[ ]:


