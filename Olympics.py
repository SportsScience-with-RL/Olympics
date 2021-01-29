#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


df_main = pd.read_csv(r'C:\Users\raflg\Desktop\summer.csv')

df_main.head()


# In[3]:


df_main.shape


# In[4]:


df_main.dtypes


# # Clean up the data

# In[5]:


df_main.isnull().sum()


# In[6]:


null_df = df_main[df_main.isnull().any(axis=1)]
null_df


# In[7]:


df_main.dropna(how='any', inplace=True)
df_main.shape


# In[8]:


df_main.duplicated().sum()
df_main.loc[df_main.duplicated(keep=False)]


# In[9]:


df_main.drop_duplicates(keep='first', inplace=True)
df_main.shape


# # Task 1: Find the Top 5 countries of the last Olympics

# In[10]:


last_comp = df_main['Year'].max()
last_olymp = df_main[df_main['Year'] == last_comp]
last_olymp


# In[11]:


top_five = last_olymp.groupby('Country').Medal.count().sort_values(ascending=False).nlargest(5)
top_five


# In[12]:


top_five_countries = ['USA', 'RUS', 'CHN', 'GBR', 'AUS']


# # Task 2: Sum up medals of the Top 5 over all the Olympics

# In[13]:


df_five = df_main[df_main['Country'].isin(top_five_countries)]
df_five


# In[14]:


df_topfive = df_five.groupby(['Year', 'Country']).agg({'Medal' : 'count'})
df_topfive.reset_index(level=['Country','Year'], inplace=True)
df_topfive.sort_values(by='Year', ascending=False, inplace=True)


# In[15]:


px.bar(df_topfive, x='Medal', y='Country', animation_frame='Year', range_x=[0,400])


# ## Task 3: Compare Top 5 Gold Medal % in North vs. South Hemisphere

# In[16]:


df_five.City.unique()


# In[17]:


df_five[df_five['City'] == 'Melbourne / Stockholm'].Sport.unique()


# In[130]:


hemisphere_conditions = [(df_five['City'] == 'Athens') | (df_five['City'] == 'Paris') | (df_five['City'] == 'St Louis') |
                        (df_five['City'] == 'London') | (df_five['City'] == 'Stockholm') | (df_five['City'] == 'Antwerp') |
                        (df_five['City'] == 'Amsterdam') | (df_five['City'] == 'Los Angeles') | (df_five['City'] == 'Berlin') |
                        (df_five['City'] == 'Helsinki') | (df_five['City'] == 'Rome') | (df_five['City'] == 'Tokyo') |
                        (df_five['City'] == 'Mexico') | (df_five['City'] == 'Munich') | (df_five['City'] == 'Montreal') |
                        (df_five['City'] == 'Moscow') | (df_five['City'] == 'Barcelona') | (df_five['City'] == 'Atlanta') |
                        (df_five['City'] == 'Beijing'),
                        (df_five['City'] == 'Seoul') | (df_five['City'] == 'Sydney'),
                        (df_five['City'] == 'Melbourne / Stockholm') & (df_five['Sport'] == 'Equestrian'),
                        (df_five['City'] == 'Melbourne / Stockholm') & (df_five['Sport'] != 'Equestrian')]

hemisphere_results = ['North Hemisphere', 'South Hemisphere', 'North Hemisphere', 'South Hemisphere']

df_five['Hemisphere'] = np.select(hemisphere_conditions, hemisphere_results)


# In[131]:


df_topfive_hem_medal = df_five.groupby(['Hemisphere', 'Country']).agg({'Medal' : 'count'})
df_topfive_hem_gold = df_five.groupby(['Hemisphere', 'Country']).agg({'Medal' : lambda x: (x=='Gold').sum()})

df_topfive_hem_gold_pct = df_topfive_hem_gold.div(df_topfive_hem_medal, level='Country')*100
df_topfive_hem_gold_pct.round()


# ## Task 4: Compare Top 5 Women and Men medals 

# In[20]:


df_five.Year.unique()


# In[21]:


df_five[df_five['Gender'] == 'Women']['Year'].unique()


# In[22]:


df_five_sub = df_five[df_five['Year'] >= 1900]
df_five_sub


# In[23]:


df_topfive_sex = df_five_sub.groupby(['Year', 'Country']).agg(Women=('Gender', lambda x: (x=='Women').sum()) , 
                                                                           Men =('Gender', lambda x: (x=='Men').sum()))
df_topfive_sex


# In[48]:


df_five_sub_medal = df_five_sub.groupby(['Year', 'Country']).agg(Women=('Medal', 'count'), Men=('Medal', 'count'))

df_topfive_sex_pct = df_topfive_sex.div(df_five_sub_medal, level='Country')*100
df_topfive_sex_pct.round()


# ## Task 5: Compare sports to find which one brought more medals over all the Olympics 

# In[119]:


df_topfive_sports = df_five.groupby(['Country', 'Discipline']).agg({'Medal' : 'count'})
df_topfive_medals = df_topfive_sports.groupby(level='Country').sum()

df_topfive_sports_pct = df_topfive_sports.div(df_topfive_medals, level='Country')*100

df_topfive_sports_pct.sort_values(['Country','Medal'], ascending=[1,0], inplace=True)
df_topfive_sports_pct.round(2)

