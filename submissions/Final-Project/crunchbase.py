import json
import requests
import time
from pprint import pprint
import pandas as pd

api_key = "?user_key=6649d8d275f35028c563aeffbc7b2cf7"
base = "https://api.crunchbase.com/v/2/"

with open('organizations.json') as jsonFile:
	organizations = json.load(jsonFile)

columns = ['name', 'location', 'description', 'founded', 'funding',
	'funding_rounds', 'ipo', 'acquisitions', 'num_employees',
	'is_closed', 'role_investor']

# create DataFrame
data = pd.DataFrame(columns=columns, index=range(0, len(organizations['items'])))

# try to get a number field
def getNumField(organizationObj, fieldName):
	numField = 0
	try:
		numField = organizationObj[fieldName]['paging']['total_items']
	except:
		pass
	return numField

# try to get a normal field
def getField(organizationObj, field):
	newField = 0
	try:
		newField = organizationObj[field]
	except:
		pass
	return newField

# try to get a location field
def getLocation(organizationObj):
	location = ''
	try:
		location += organizationObj['headquarters']['items'][0]['city'] + ', '
		location += organizationObj['headquarters']['items'][0]['region'] + ', '
		location += organizationObj['headquarters']['items'][0]['country']
	except:
		pass
	return location

# Construct dataframe
for i in range(0, len(organizations['items'])):
	print i
	if i == 1170:
		continue
	# request organization
	organization = requests.get(base + organizations['items'][i]['path'] + api_key).json()
	organization = organization['data']

	# create row
	row = {
		'name': getField(organization['properties'], 'permalink'),
		'location': getLocation(organization['relationships']),
		'description': getField(organization['properties'], 'short_description'),
		'founded': getField(organization['properties'], 'founded_on'),
		'funding': getField(organization['properties'], 'total_funding_usd'),
		'funding_rounds': getNumField(organization['relationships'], 'funding_rounds'),
		'acquisitions': getNumField(organization['relationships'], 'acquisitions'),
		'ipo': getNumField(organization['properties'], 'ipo'),
		'num_employees': getField(organization['properties'], 'number_of_employees'),
		'is_closed': getField(organization['properties'], 'is_closed'),
		'role_investor': getField(organization['properties'], 'role_investor')
	}
	data.loc[i] = pd.Series(row)

	# sleep to avoid API limit
	if i % 100 == 0 and i != 0:
		time.sleep(20)

# write dataframe to .tsv
data.to_csv('organizationDF.tsv', sep='\t', encoding='utf-8')
