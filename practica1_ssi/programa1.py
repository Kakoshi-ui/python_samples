#!/usr/bin/env python
# coding: utf-8

# In[33]:


import datetime
import os
import shutil


# In[34]:


dt = datetime.datetime.now()


# In[35]:


nombre = "Copia de seguridad creada el dia {} del año {} y la hora {} mes {} minuto {}".format(dt.day,dt.year,dt.hour,dt.month,dt.minute)


# In[36]:


shutil.make_archive(nombre,"zip","carpeta_respaldo")


# In[37]:


comienzo = []


# In[38]:


total = os.listdir()


# In[39]:


for a in total:
    if a.startswith("Copia de seguridad creada") == True:
        comienzo.append(a)


# In[40]:


rutadestino = "C:/Users/axel9/Documents/Seguridad_Sis"


# In[41]:


for i in comienzo:
    shutil.move(i,rutadestino)


# In[ ]:




