import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawler():
    year = 1997
    row = []
    while year <2017:
        year+=1
        month=1
        while month < 13:

            source = requests.get('https://www.christies.com/results?sc_lang=en&month=' + str(month) + '&year=' + str(year) ).text
            soup = BeautifulSoup(source, 'html.parser')

            for all in soup.find_all('li'):
                for date in all.findAll('h4'):
                    dates = date.text
                    row.append(dates)
                for rest in all.findAll('div',{'class':"col-xs-12 col-sm-12 col-md-5 col-lg-5 sale--items--item--image-description image-description"}):
                    for name in rest.findAll('a'):
                        names = name.text
                        row.append(names)
                    for place in rest.findAll('span',{'class':"image-description--location hidden-xs hidden-sm p--primary_large"}):
                        places = place.text
                        row.append(places)
                    for price in rest.findAll('div',{'class':"col-xs-12 col-sm-12 image-description--sale-total p--primary_large"}):
                        prices = price.text[14:30]
                        row.append(prices)
                df = pd.DataFrame({"date": (row[0::4]), "Name": (row[1::4]), "Location": (row[2::4]), "Sold Price": (row[3::4])})
            month += 1
            df.to_csv('All_Auction_House_Events.csv')
crawler()
