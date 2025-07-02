# %%
import pandas as pd
import numpy as np
import requests as rq
import json

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
# %%
''' 
Data:
-AAIA
-Brand
-Sure
-eBay
-Bigcommerce = website
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
aaiaCode = "BKQC"
brand = "Banks Power"
sure = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\20250701-202737-187532-products-export.csv')
eBay = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\eBay-all-active-listings-report-2025-06-30-11237259049.csv',skiprows=1)
website = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\products-2025-07-01.csv')
att = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Attributes_F1.txt',
    sep="|",
    skiprows=1)
des = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Description_C1.txt',
    sep="|",
    skiprows=1)
dad = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Digital_Assets_Descriptions_P64.txt',
    sep="|",
    skiprows=1)
dap = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Digital_Assets_P.txt',
    sep="|",
    skiprows=1)
exp = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_EXPI_E1.txt',
    sep="|",
    skiprows=1)
hmj = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Hazardous_Material_J1.txt',
    sep="|",
    skiprows=1)
hs1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Header_Segment_A1.txt',
    sep="|",
    skiprows=1)
in1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Interchange_N1.txt',
    sep="|",
    skiprows=1)
isb = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Item_Segment_B1.txt',
    sep="|",
    skiprows=1)
kit = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Kits_K1.txt',
    sep="|",
    skiprows=1)
mca = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Market_Copy_A80.txt',
    sep="|",
    skiprows=1)
md1 =  pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Market_Copy_Digital_Assets_M01.txt',
    sep="|",
    skiprows=1)
md6 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Market_Copy_Digital_Assets_M64.txt',
    sep="|",
    skiprows=1)
pac = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Packaging_H1.txt',
    sep="|",
    skiprows=1)
psa = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Price_Sheet_A50.txt',
    sep="|",
    skiprows=1)
pd1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\BanksPower_Pricing_D1.txt',
    sep="|",
    skiprows=1)



'''
Have to clean the website and suredone data
Filter it down to only the brand
'''
website.drop(website.columns[range(78,333)],axis=1,inplace=True)
website = website.dropna(axis=1,how='all')
sure = sure.dropna(axis=1,how='all')
eBay = eBay.dropna(axis=1,how='all')
 # %%
'''
All of these files are in XML so I am going to try pivot it out into a more flat way
'''
expFlat = exp.pivot(index='Part Number',columns='EXPI Code',values='EXPI Data')
pd1Flat = pd1.pivot(index='Part Number ',columns='Price Type',values='Price')


# %%
website = website[website['Brand Name'] == "Banks Power"]
sure = sure[sure['guid'].str.contains(aaiaCode,case=False,na=False)]
eBay = eBay[(eBay['Title'].str.contains("Banks",case=False,na=False)) + 
            (eBay['Listing site'] == 'US')]

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
'''
Suredone is our source of truth so we are going to run a few checks:
-Pricing (MAP) 
-New Product
-Discontinued Product
    -From SD
    -From Turn
Some of these checks can be done sheet to sheet
Anything that uses a call should filter it down to only the necessary rows
'''
# %%
'''
First step is identifying all specific listings: 
- (House) are not going to be managed via this application
- COMBO are kits that are made up of multiple items and should be handled and seperated differently
- SNRV are managed independently and locally on each website
- -AAIA code are managed by suredone and can be changed via a suredone import
1. Find the House on eBay / Suredone / Website and drop them
2. Combos go into a file call kits
3. SNRV
4. Sure has all AAIA coded, and website and ebay SNRV will have the local changes
'''
sure = sure[~sure['guid'].str.contains("house",na=False, case=False)]
sure = sure[~sure['guid'].str.contains("SNRV",na=False, case=False)]
sureKits = sure[sure['guid'].str.contains("combo",na=False, case=False)]
sure = sure[~sure['guid'].str.contains("combo",na=False, case=False)]

eBay = eBay[~eBay['Custom label (SKU)'].str.contains("house",na=False, case=False)]
eBaySNRV = eBay[eBay['Custom label (SKU)'].str.contains("SNRV",na=False, case=False)]
eBay = eBay[~eBay['Custom label (SKU)'].str.contains("SNRV",na=False, case=False)]
eBayKits = eBay[eBay['Custom label (SKU)'].str.contains("combo",na=False, case=False)]
eBay = eBay[~eBay['Custom label (SKU)'].str.contains("combo",na=False, case=False)]

website = website[~website['Product Code/SKU'].str.contains("house",na=False, case=False)]
websiteSNRV = website[website['Product Code/SKU'].str.contains("SNRV",na=False, case=False)]
website = website[~website['Product Code/SKU'].str.contains("SNRV",na=False, case=False)]
websiteKits = website[(website['Product Code/SKU'].str.contains("/",na=False, case=False)) + 
                      (website['Product Code/SKU'].str.contains(" ",na=False, case=False)) + 
                      (website['Product Code/SKU'].str.contains("combo",na=False, case=False))]
website = website[~(website['Product Code/SKU'].str.contains("/",na=False, case=False)) + 
                      (website['Product Code/SKU'].str.contains(" ",na=False, case=False)) + 
                      (website['Product Code/SKU'].str.contains("combo",na=False, case=False))]
# %%
'''
Discontinued List
1. Has a discontinued or is not found SD 
2. Check Inventory in Keystone if not found
3. Send API request for inventory in Turn 14 if not found
4. Generate potential discontinued list
'''

# %%
'''
Pricing
'''
# %%
