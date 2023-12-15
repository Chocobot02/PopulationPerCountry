from bs4 import BeautifulSoup as soup
import requests as req
from functions import save,scrape


root = 'https://www.worldometers.info'
website = f'{root}/world-population/population-by-country'
req_site = req.get(url=website).text

content = soup(req_site,'lxml')

countrycontent = content.find('table', id='example2')
countryrow = countrycontent.find('tbody').find_all('tr')

for row in countryrow:
    data = row.find_all('td')
    link = data[1].find('a')
    landsize = data[6].text
    rownum = int(data[0].text.strip())

   # since starting from 201 the table format change
    if rownum <= 200:
        # extract the data
        information = scrape.format1scrapeinfo(link['href'], link.text, landsize)
        # load or save the collected data 
        save.savetomysql(information)
    else:
        # extract the data
        information = scrape.format2scrapeinfo(link['href'], link.text, landsize)
        # load or save the collected data 
        save.savetomysql(information)

    
