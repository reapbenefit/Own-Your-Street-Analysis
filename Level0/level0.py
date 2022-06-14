#Google Doc
#https://docs.google.com/document/d/1UIpHRg897H433i2Vzbk6wWlGkUNyVned_UzZk09NjVI/edit

## Google Sheet for Level 0
#https://docs.google.com/spreadsheets/d/1qf5nOCTAzAC63YvsMcLGTL5DhsQiQl1q2b-mvo-TA74/edit#gid=797785735

import collections
import pandas as pd
import numpy as np
import gspread 
from google.oauth2 import service_account
import emoji
import plotly.express as px

# Load our data set which is the google sheet

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'gsheet.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


gc = gspread.authorize(credentials)

worksheet = gc.open_by_key('1XTQiudjwLorlookKuKKpW53KD5YpVNk9bCInUgN4JEA').sheet1
rows = worksheet.get_all_values()

# Convert google sheet data to data frame

df = pd.DataFrame(rows[1:], columns=rows[0])
df[df==""] = np.NaN
df.fillna(method="ffill",inplace=True)
print(df.head())
print('---------------------------------------------------------')
print("Total Responses: ",df.shape[0])

def remove_duplicate(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)
    return res

name=[]

for i in range(0,len(df)):
    name.append(df.loc[i,"name"])
    
name=remove_duplicate(name)

ID=[]
ID_list=[]

for i in range(0,len(df)):
    ID.append(df.loc[i,"number"])
    ID_list.append(df.loc[i,"number"])
    
ID=remove_duplicate(ID)
print("Total Unique Responses: ",len(ID))


date=[]
for i in range(0,len(df)):
    date.append(df.loc[i,"date"])

day_count=dict(collections.Counter(date))
day_df = pd.DataFrame.from_dict(day_count, orient ='index')
day_df.columns = ['count']
print("Activity Count Per Day")
print(day_df)

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


emoji_count=0
for j in range(0,len(name)):
    if (text_has_emoji(name[j])==True):
        emoji_count+=1

print("Total number of names with emojis: ",emoji_count)


ans1=0
for m in range(0,len(df)):
    if(df.loc[m,"q1"]=="Yes"):
        ans1=ans1+1
        
print("Streets with 10+ trees: ",ans1)


ans2=0
for n in range(0,len(df)):
    if(df.loc[n,"q2"]=="Yes"):
        ans2=ans2+1
        
print("Streets with working street lights: ",ans2)



potholes=[]
for k in range(0,len(df)):
    potholes.append(df.loc[k,"q3"])

potholes_count=dict(collections.Counter(potholes))

potholes_stat=[]
potholes_num=[]


potholes_stat=list(potholes_count.keys())
potholes_num=list(potholes_count.values())

fig = px.pie(values=potholes_num, names=potholes_stat, title='Number of Potholes', color=potholes_stat,
             color_discrete_map={potholes_stat[0]:'#1F618D',
                                 potholes_stat[1]:'#82E0AA ',
                                 potholes_stat[2]:'#E74C3C',
                                })
fig.show()
