# %%
import pandas as pd
import numpy as np
import requests as rq
import json
# %%
''' 
Data:
-AAIA
-Sure
We have a PIES file it contains:
-Attributes
-Description
-Digital_Asset_Description
-Digital_Assets
-EXPI_E1
-Hazardous_Materials_J1
-Header_Segment_A1
-Interchange_N1
-Item_Segment_B1
-Kits_K1
-Market_Copy_A80
-Market_Copy_Digital_Assets_M01
-Market_Copy_Digital_Assets_M64
-Packaging_H1
-Price_Sheeet_A50
-Pricing_D1

'''

sure = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\20250625-190922-1810-products-export.csv')
att = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Attributes_F1.txt',
    sep="|",
    skiprows=1)
des = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Description_C1.txt',
    sep="|",
    skiprows=1)
dad = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Digital_Assets_Descriptions_P64.txt',
    sep="|",
    skiprows=1)
dap = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Digital_Assets_P.txt',
    sep="|",
    skiprows=1)
exp = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Digital_Assets_P.txt',
    sep="|",
    skiprows=1)
hmj = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Hazardous_Material_J1.txt',
    sep="|",
    skiprows=1)
hs1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Header_Segment_A1.txt',
    sep="|",
    skiprows=1)
in1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Interchange_N1.txt',
    sep="|",
    skiprows=1)
isb = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Item_Segment_B1.txt',
    sep="|",
    skiprows=1)
kit = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Kits_K1.txt',
    sep="|",
    skiprows=1)
mca = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Market_Copy_A80.txt',
    sep="|",
    skiprows=1)
md1 =  pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Market_Copy_Digital_Assets_M01.txt',
    sep="|",
    skiprows=1)
md6 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Market_Copy_Digital_Assets_M64.txt',
    sep="|",
    skiprows=1)
pac = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Packaging_H1.txt',
    sep="|",
    skiprows=1)
psa = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Price_Sheet_A50.txt',
    sep="|",
    skiprows=1)
pd1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\RealTruckInc_Pricing_D1.txt',
    sep="|",
    skiprows=1)
# %%
'''
It needs to do the following:
A list of map pricing changes
Pull pricing from warehouses:
-Turn 14
-Premier
-Keystone
-Meyers
'''
keystone = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Inventory.csv')
# %%
'''
Requests
Turn 14 Token
'''
turnUrl = "https://api.turn14.com/"
creds = open(r"C:\Users\Owner\Desktop\git\creds.json")
client = json.load(creds)["turn14"].get("client")
creds = open(r"C:\Users\Owner\Desktop\git\creds.json")
secret = json.load(creds)["turn14"].get("secret")
creds.close()
Turnaccess = rq.post(turnUrl+"v1/token",data={'grant_type' : 'client_credentials',
                                      'client_id':client,
                                      'client_secret': secret})
turnToken = Turnaccess.json().get("access_token")
# %%
'''
Requests
Premier Token
'''
premTestUrl = "http://api-test.premierwd.com/api/v5/"
premProdUrl = "https://api.premierwd.com/api/v5/"
creds = open(r"C:\Users\Owner\Desktop\git\creds.json")
premApiKey = json.load(creds)["premier"].get("apiKey")
premierAccess = rq.get(premProdUrl+"authenticate",params={"apiKey": premApiKey})
premierToken = premierAccess.json().get("sessionToken")
creds.close()
# %%
'''
Requests
Meyer Token
'''
meyerTestUrl = "https://meyerapitest.meyerdistributing.com/http/default/TestAPI/v2/"
meyerProdUrl = "https://meyerapi.meyerdistributing.com/http/default/ProdAPI/v2/"
creds = open(r"C:\Users\Owner\Desktop\git\creds.json")
meyerToken = json.load(creds)["meyer"].get("prod")
creds.close()
# %%
