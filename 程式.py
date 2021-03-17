#因為資料量龐大導致筆電無法負荷，故只先匯入a_lvr_land_a、b_lvr_land_a兩個檔案七個欄位
#Untitled1.ipynb為原版程式(使用jupyter notebook)

import pandas as pd
import csv
import numpy as np
import xml.etree.ElementTree as et 

#讀取XML(a_lvr_land_a)
xtree = et.parse("a_lvr_land_a.xml")
xroot = xtree.getroot()
df_cols = ["鄉鎮市區", "交易標的","土地區段","主要用途","建物型態","總樓層數","主要建材"]
rows = []

for node in xroot: 
    s1_loc = node.find("鄉鎮市區").text
    s1_subject = node.find("交易標的").text
    s1_section = node.find("土地區段位置建物區段門牌").text
    s1_use = node.find("主要用途").text
    s1_type = node.find("建物型態").text
    s1_floor = node.find("總樓層數").text
    s1_material = node.find("主要建材").text
    rows.append({"鄉鎮市區": s1_loc, "交易標的": s1_subject,"土地區段":s1_section, "主要用途":s1_use,"建物型態":s1_type,"總樓層數":s1_floor,"主要建材":s1_material})

df_a = pd.DataFrame(rows, columns = df_cols)

#df_a有519筆
#df_a[0:3]

#讀取XML(b_lvr_land_a)
xtree = et.parse("b_lvr_land_a.xml")
xroot = xtree.getroot()
df_cols = ["鄉鎮市區", "交易標的","土地區段","主要用途","建物型態","總樓層數","主要建材"]
rows = []

for node in xroot: 
    s2_loc = node.find("鄉鎮市區").text
    s2_subject = node.find("交易標的").text
    s2_section = node.find("土地區段位置建物區段門牌").text
    s2_use = node.find("主要用途").text
    s2_type = node.find("建物型態").text
    s2_floor = node.find("總樓層數").text
    s2_material = node.find("主要建材").text
    rows.append({"鄉鎮市區": s2_loc, "交易標的": s2_subject,"土地區段":s2_section, "主要用途":s2_use,"建物型態":s2_type,"總樓層數":s2_floor,"主要建材":s2_material})

df_b = pd.DataFrame(rows, columns = df_cols)

#df_b有854筆
#df_b[0:3]

#先把df_a加入到df_all裡面
df_all = pd.DataFrame()

df_all.insert(0,"a_鄉鎮市區",df_a["鄉鎮市區"])
df_all.insert(1,"a_交易標的",df_a["交易標的"])
df_all.insert(2,"a_土地區段",df_a["土地區段"])
df_all.insert(3,"a_主要用途",df_a["主要用途"])
df_all.insert(4,"a_建物型態",df_a["建物型態"])
df_all.insert(5,"a_總樓層數",df_a["總樓層數"])
df_all.insert(6,"a_主要建材",df_a["主要建材"])

#再把df_b加入到df_all裡面(放在df_a之後)(1373筆)
location = 519
for i in range(len(df_b)):
    df_all.loc[location] = [df_b["鄉鎮市區"][i],df_b["交易標的"][i],df_b["土地區段"][i],df_b["主要用途"][i],df_b["建物型態"][i],df_b["總樓層數"][i],df_b["主要建材"][i]]
    location = location + 1

#新增"層數"欄位，把中文的總樓層數轉換成數字
df_all.columns = ["a_鄉鎮市區","a_交易標的","a_土地區段","a_主要用途","a_建物型態","a_總樓層數","a_主要建材","層數"]
for i in range(len(df_all)):
     #print(df_all["a_總樓層數"][i])
    layer = 0
    if(df_all["a_總樓層數"][i]==None):
        continue
    for j in range(len(df_all["a_總樓層數"][i])):
        
        if(df_all["a_總樓層數"][i][j]!="十" and df_all["a_總樓層數"][i][j]!="層"):
            layer = layer+numeric(df_all["a_總樓層數"][i][j])
        if(df_all["a_總樓層數"][i][j]=='十' and j==0):
            layer = 10
        if(df_all["a_總樓層數"][i][j]=='十' and j!=0):
            layer = layer * 10
    #print(layer)
    df_all["層數"][i] = layer

#df_all[0:5]

from unicodedata import numeric
#從df_all找符合的三個條件
used = pd.DataFrame(pd.np.empty((0, 7)))  
used.columns = ["新鄉鎮市區","新交易標的","新土地區段","新主要用途","新建物型態","新總樓層數","新主要建材"]
index = 0
for i in range(len(df_all)):
    if(df_all["a_主要用途"][i]=="住家用"):
        if "住宅大樓" in df_all["a_建物型態"][i]:
            if(df_all["層數"][i]>=13):
                used.loc[index] = [df_all["a_鄉鎮市區"][i],df_all["a_交易標的"][i],df_all["a_土地區段"][i],df_all["a_主要用途"][i],df_all["a_建物型態"][i],df_all["a_總樓層數"][i],df_all["a_主要建材"][i]]
                index = index + 1

#used[0:5]

used.to_csv (r'C:\Users\acer\Desktop\download\filter_a.csv', index = False, header=True)




