# Install and import requests package
import requests

# Install and import beautifulsoup package
from bs4 import BeautifulSoup

# import python common package to save data into file
from time import sleep
import os
import csv
import re

# Send request to get response object from webpage server
with requests.Session() as session:
    response = session.get('https://www.etsy.com/search?q=gift%20for%20women', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'})

sleep(5)

# Parse response object with beautifulsoup4
content = BeautifulSoup(response.text, 'html.parser')
session.close()

# Get data from html document by select method beautifulsoup
data={'url':'', 'title':'', 'price':'', 'sales':''}
result = content.select('ol.wt-grid.wt-grid--block.wt-pl-xs-0.tab-reorder-container > li')
res=[]
for i in result:
    try:
        data['url'] = i.select_one('a.listing-link.wt-display-inline-block')['href']
    except TypeError:
        break
    data['title'] = i.select_one('h3.wt-text-caption.v2-listing-card__title').text
    data['title'] = re.sub(r'\n +', '', data['title'])
    data['price'] = i.select_one('div.n-listing-card__price.wt-display-flex-xs.wt-align-items-center > p.wt-text-title-01.lc-price > span:nth-of-type(2)').text
    data['price'] = re.sub(r'\D', '', data['price'])
    try:
        data['sales'] = i.select_one('span.wt-text-caption.wt-text-gray.wt-display-inline-block.wt-nudge-l-3.wt-pr-xs-1').text
        data['sales'] = re.sub(r'\D', '', data['sales'])
    except AttributeError:
        data['sales'] = 0
    res.append(data.copy())
print(res)
print(f'{len(res)} products collected by request and bs4')

# Save data into file csv
filepath = 'C:/project/etsysoup/result/result.csv'
print('Creating file...')
folder = filepath.rsplit("/", 1)[0]
try:
    os.mkdir(folder)
except FileExistsError:
    pass
with open(filepath, 'w+', encoding="utf-8", newline='') as f:
    headers = ['url', 'title', 'price', 'sales']
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for i in res:
        writer.writerow(i)
    f.close()
print(f'{filepath} created')