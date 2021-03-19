import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import numpy as np
import os

def ddd(a):
    for mName, mNum in [("január", "01"), ("február", "02"), ("március", "03"), ("április", "04"), ("május", "05"), ("június", "06"), ("július", "07"), ("augusztus", "08"), ("szeptember", "09"), ("október", "10"), ("novermber", "11"), ("december", "12")]:
        if mName in a:
            aSub = a.replace(mName, mNum)
            return str(datetime.strptime(aSub, '%Y. %m %d.').date())
        else:
            continue

page = requests.get("https://www.idokep.hu/idojaras/Budapest")
soup = BeautifulSoup(page.content, "html.parser")

ftDict = {"ScDay":[], "ScTime":[], "Day":[], "Date":[], "TempMax":[], "TempMin":[], "W1":[], "W2":[]}
td = datetime.today().strftime('%Y-%m-%d')

s1 = soup.select("div.dailyForecastCol div.dfIconAlert a")
s2 = soup.select("div.dailyForecastCol div.min-max-container div.max a")
s3 = soup.select("div.dailyForecastCol div.min-max-container div.min a")
s4 = soup.select("div.dailyForecastCol div.dfIconAlert a")

for i in range(0,len(s1)):
    ftDict["ScDay"].append(td)
    if datetime.now().strftime("%H:%M:%S") > '12:00:00':
        ftDict["ScTime"].append(22)
    else:
        ftDict["ScTime"].append(10)
    ftDict["Day"].append(s1[i]["title"].split("<br>")[0])
    ftDict["Date"].append(s1[i]["title"].split("<br>")[1])
    ftDict["TempMax"].append(s2[i].text)
    ftDict["TempMin"].append(s3[i].text)

    k2 = re.sub('<[^>]+>', '', s4[i]["data-content"].replace("\r\n", ""))
    k3 = [i for i in k2.split("  ") if i != ""]
    ftDict["W1"].append(k3[0])
    if len(k3) > 1:
        ftDict["W2"].append(k3[1])
    else:
        ftDict["W2"].append(np.nan)

df = pd.DataFrame(ftDict)

df["DateFormat"] = df["Date"].apply(lambda x: ddd(x.lower())

if "akaka.csv" in os.listdir(os.curdir):
    dfBase = pd.read_csv("akaka.csv", index_col=[0])
    pd.concat([dfBase, df]).reset_index(drop=True).to_csv("akaka.csv")
else:
    df.to_csv("akaka.csv")
