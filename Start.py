# %%
import pandas as pd
import numpy as np
import requests as rq
import json
import os

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
aaiaCode = "BKLD"
brand = "Injen"
sure = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\20250729-204451-1286-products-bkld-export.csv')
eBay = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\eBay-all-active-listings-report-2025-07-29-12255560032.csv')
website = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\products-2025-07-29 (1).csv')
att = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Attributes_F1.txt',
    sep="|",
    skiprows=1)
des = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Description_C1.txt',
    sep="|",
    skiprows=1)
dad = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Digital_Assets_Descriptions_P64.txt',
    sep="|",
    skiprows=1)
dap = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Digital_Assets_P.txt',
    sep="|",
    skiprows=1)
exp = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_EXPI_E1.txt',
    sep="|",
    skiprows=1)
hmj = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Hazardous_Material_J1.txt',
    sep="|",
    skiprows=1)
hs1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Header_Segment_A1.txt',
    sep="|",
    skiprows=1)
in1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Interchange_N1.txt',
    sep="|",
    skiprows=1)
isb = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Item_Segment_B1.txt',
    sep="|",
    skiprows=1)
kit = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Kits_K1.txt',
    sep="|",
    skiprows=1)
mca = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Market_Copy_A80.txt',
    sep="|",
    skiprows=1)
md1 =  pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Market_Copy_Digital_Assets_M01.txt',
    sep="|",
    skiprows=1)
md6 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Market_Copy_Digital_Assets_M64.txt',
    sep="|",
    skiprows=1)
pac = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Packaging_H1.txt',
    sep="|",
    skiprows=1)
psa = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Price_Sheet_A50.txt',
    sep="|",
    skiprows=1)
pd1 = pd.read_csv(
    r'C:\Users\Owner\Desktop\git\Data\Injen_Pricing_D1.txt',
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
website = website[website['Brand Name'] == "Injen"]
sure = sure[sure['guid'].str.contains(aaiaCode,case=False,na=False)]
eBay = eBay[
    (eBay['Title'].str.contains("Injen",na=False, case=False)) & 
    (eBay["Listing site"] == "US")]
website.rename(columns={"Manufacturer Part Number" : "mpn"},inplace=True)
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
keystone.PartNumber = keystone.PartNumber.str[2:-1]
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
GET/v1/brands
Retrieve a list of all brands that Turn 14 carries

NOTE: Use the id attribute from this endpoint as the brand_id parameter on the inventory or pricing endpoints to pull information for specific brands
'''
brandCode = rq.get(turnUrl+"v1/brands",headers={'Authorization':"Bearer " +turnToken},data={"Content-Type":'application/json'})
# %%
brandCodeDF = pd.DataFrame()
brandCodeDF["AAIA"] = pd.Series()
brandCodeDF["id"] = pd.Series()
for index, brand in enumerate(brandCode.json().get('data')):
    try:
        brandCodeDF[index,"AIAA"] = brand.get("attributes").get("AAIA")[0]
    except:
        brandCodeDF[index,"AIAA"] = brand.get("attributes").get("AAIA")
    brandCodeDF[index,"id"] = brand.get("id")
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
sureKits = sure[sure['guid'].str.contains("kit",na=False, case=False)]
sure = sure[~sure['guid'].str.contains("kit",na=False, case=False)]

eBay = eBay[~eBay['Custom label (SKU)'].str.contains("house",na=False, case=False)]
eBaySNRV = eBay[eBay['Custom label (SKU)'].str.contains("SNRV",na=False, case=False)]
eBaySNRV["mpn"] = eBaySNRV["Custom label (SKU)"].str[4:-5]
eBay = eBay[~eBay['Custom label (SKU)'].str.contains("SNRV",na=False, case=False)]
eBayKits = eBay[eBay['Custom label (SKU)'].str.contains("combo",na=False, case=False)]
eBayKits["mpn"] = eBayKits["Custom label (SKU)"].str[5:-5]
eBay = eBay[~eBay['Custom label (SKU)'].str.contains("combo",na=False, case=False)]
eBay["mpn"] = eBay["Custom label (SKU)"].str[:-5]


website = website[~website['mpn'].str.contains("house",na=False, case=False)]
websiteSNRV = website[website['mpn'].str.contains("SNRV",na=False, case=False)]
website = website[~website['mpn'].str.contains("SNRV",na=False, case=False)]
websiteKits = website[(website['mpn'].str.contains("/",na=False, case=False)) + 
                      (website['mpn'].str.contains(" ",na=False, case=False)) + 
                      (website['mpn'].str.contains("combo",na=False, case=False))]
website = website[~(website['mpn'].str.contains("/",na=False, case=False)) + 
                      (website['mpn'].str.contains(" ",na=False, case=False)) + 
                      (website['mpn'].str.contains("combo",na=False, case=False))]
# %%                  
'''
Merge DFs
'''
mergedeBay = pd.merge(
    eBay,expFlat,how="left",left_on="mpn",right_index=True)
mergedeBay = pd.merge(
    mergedeBay,pd1Flat,how="left",left_on="mpn",right_index=True)
mergedeBaySNRV = pd.merge(
    eBaySNRV,expFlat,how="left",left_on="mpn",right_index=True)
mergedeBaySNRV = pd.merge(
    mergedeBaySNRV,pd1Flat,how="left",left_on="mpn",right_index=True)
mergedSure = pd.merge(
    sure,expFlat,how="left",left_on="mpn",right_index=True)
mergedSure = pd.merge(
    mergedSure,pd1Flat,how="left",left_on="mpn",right_index=True)
mergedWebsite = pd.merge(
    website,expFlat,how="left",left_on="Product Code/SKU",right_index=True)
mergedWebsite = pd.merge(
    mergedWebsite,pd1Flat,how="left",left_on="Product Code/SKU",right_index=True)
mergedWebsiteSNRV = pd.merge(
    websiteSNRV,expFlat,how="left",left_on="Product Code/SKU",right_index=True)
mergedWebsiteSNRV = pd.merge(
    mergedWebsiteSNRV,pd1Flat,how="left",left_on="Product Code/SKU",right_index=True)

# %%
'''
Discontinued List
1. Has a discontinued or is not found SD 
2. Check Inventory in Keystone if not found
3. Generate upload files
4. 

'''
eBayDis = mergedeBay[~mergedeBay["LIS"].str.contains("Available To Order",case=False,na=False)]
eBayDisSNRV = mergedeBaySNRV[~mergedeBaySNRV["LIS"].str.contains("Available To Order",case=False,na=False)]
sureDis = mergedSure[~mergedSure["LIS"].str.contains("Available To Order",case=False,na=False)]
websiteDis = mergedWebsite[~mergedWebsite["LIS"].str.contains("Available To Order",case=False,na=False)]
websiteDisSNRV = mergedWebsiteSNRV[~mergedWebsiteSNRV["LIS"].str.contains("Available To Order",case=False,na=False)]

disList = []
disList.append(eBayDis)
disList.append(eBayDisSNRV)
disList.append(sureDis)
disList.append(websiteDis)
disList.append(websiteDisSNRV)

keyList = []
for df in disList:
    if not(df.empty):
        df = pd.merge(df,keystone[["PartNumber","TotalQty"]],left_on='mpn',right_on='PartNumber',how='left')
        keyList.append(df)

keyList[0]

eBayRM = pd.DataFrame()
eBayRM["Item number"] = keyList[0]["Item number"]
eBayRM["EndingReason"] = "NotAvailable"
eBayRM["Action"] = "End"

sureRM = pd.DataFrame()
sureRM["action=Delete"] = pd.Series()
sureRM["guid"] = sureDis["guid"]


websiteRM = pd.DataFrame()
websiteRM.index = websiteDis.index
websiteRM["Product ID"] = websiteDis["Product ID"]
websiteRM["Product Name"] = websiteDis["Product Name"]
websiteRM["Category"] = "Delete"

# %%
os.makedirs('Results',exist_ok=True)
eBayRM.to_csv("Results/eBayRM.csv",index=False)
sureRM.to_csv("Results/sureRM.csv",index=False)
websiteRM.to_csv("Results/websiteRM.csv",index=False)
# %%
'''
Pricing
'''

# %%
