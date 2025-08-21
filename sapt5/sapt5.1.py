from logging import root
import urllib
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.wikipedia.org'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

for i, img in enumerate(soup.find_all('img')):
    img_src = img.get('src')
    if img_src:
        # Convert relative URL to absolute
        img_url = urljoin(url, img_src)
        try:
            img_data = requests.get(img_url).content
            filename = f'image_{i}.jpg'
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f'Saved {filename}')
        except Exception as e:
            print(f"Couldn't download {img_url}: {e}")




"""
# 1. Write a Python script that fetches the HTML content of https://webscraper.io/test-sites/e-commerce/static
# and prints all the hyperlinks (href attributes of <a> tags) found on the page

url='https://webscraper.io/test-sites/e-commerce/static'
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')
for link in soup.find_all('a'): #Iterates over all <a> tags in the parsed HTML
   print(link.get('href'))
   

# 2. Write a Python script that fetches the HTML content of https://webscraper.io/test-sites/e-commerce/static
# and prints all prices


url='https://webscraper.io/test-sites/e-commerce/static'
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')
prices = soup.find_all('span', itemprop='price')
for price in prices: #Iterates over all <a> tags in the parsed HTML
    print(price.text)


    # 3. Write a Python script that downloads all images (src attributes of <img> tags) from https://example.com
# and saves them locally


url = 'https://example.com'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

for i, img in enumerate(soup.find_all('img')):
    if img.get('src'):
        img_data = requests.get(img['src']).content
        with open(f'image_{i}.jpg', 'wb') as f:
            f.write(img_data)
        print(f'Am salvat image_{i}.jpg')



#4. Write a Python script that scrapes all rows from the table on https://www.w3schools.com/html/html_tables.asp
# and saves the data into a CSV file

url = 'https://www.w3schools.com/html/html_tables.asp'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', class_='ws-table-all')
rows = table.find_all('tr')

with open('table_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow([cell.text.strip() for cell in row.find_all(['th', 'td'])])



# 5. Write a Python script that scrapes product names from the first 3 pages of
# https://webscraper.io/test-sites/e-commerce/static/computers/laptops and prints them
"""

import requests
from bs4 import BeautifulSoup

base_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
tick_start=time.time()
for page in range(1, 4):
    url = f"{base_url}?page={page}"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('a', class_='title')

    print(f"\nPage {page} Products:")
    for product in products:
        print(product.text.strip())
end_tick=time.time()
print(f"{(end_tick-tick_start)*1000} ms")
