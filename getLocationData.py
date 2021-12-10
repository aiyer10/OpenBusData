import pandas as pd 
import requests
import json
import xmltodict
from datetime import datetime
from tqdm import tqdm



API_KEY = r'd3cef665597dcecdb6904a8cb9179f092b768725'
url = r'https://data.bus-data.dft.gov.uk/api/v1/datafeed/?api_key=d3cef665597dcecdb6904a8cb9179f092b768725'

print("Making requests to the API")
response = requests.get(url)
data = xmltodict.parse(response.content)
# print(response)

print("Response received, processing data..")
df = pd.DataFrame()

for a , b in data.items():
	# print(b)
	
	for c, d in (b['ServiceDelivery']).items():
		# print(d)
		if isinstance(d, dict):
			for k, v in d.items():
				# print(k)
				print("Checking VehicleActivity...")
				if k =='VehicleActivity':
					for i in tqdm(v):
						list1 = []
						for m, n in i.items():
							if m=='RecordedAtTime':
								list1.append(n)
							elif m=='ItemIdentifier':
								list1.append(n)
								
							elif m=='MonitoredVehicleJourney':
								list1.append(((n['VehicleLocation'])['Latitude'])) 
								list1.append(((n['VehicleLocation'])['Longitude'])) 
								list1.append(n['OperatorRef'])
								list1.append(n['VehicleRef'])
								if ('OriginRef' in n) and ('DestinationRef' in n):
									list1.append(n['OriginRef'])
									list1.append(n['DestinationRef'])
								else :
									list1.append('')
									list1.append('')
						
						t1 = pd.DataFrame(list1)
						t2 = t1.T
						t2.columns = ['Time','ItemIdentifier','Latitude','Longitude','Operator', 'VehicleRef', 'OriginRef','DestinationRef']
						df = pd.concat([df,t2], sort=False)
df.reset_index(inplace=True)

x = str(datetime.now())[0:19]
x = x.replace(':','_')

print("Processing done at ", str(datetime.now()))
df.to_csv(r'/Users/ananth/Documents/OpenBusData/Data/locationData-'+x+r'.csv', index=None)
print('done')
