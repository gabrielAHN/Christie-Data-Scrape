import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome("C:\\Users\\Gabriel Hidalgo\\PycharmProjects\\scraper\\chromedriver.exe")
a = pd.read_csv('Amount.csv')

#Here I am taking the csv excel sheet from the Selenium web crawler and finding all null values the the initial scrape missed. This
#code goes over those rows that have a null value in the amount of item sold and retrieves the missed values, and collects all those
#into a csv. After I connect this csv with the orginal csv to fill in all the missing values from all the pages of the orginal data
#scrape.

a = a[a['Item Sold'].isnull()]

row = []

for link in a['Links']:
    try:
        driver.get(link)
        driver.implicitly_wait(15)
        try:
            driver.find_element_by_xpath('//*[@id="close_signup"]').click()
            driver.implicitly_wait(3)
            driver.find_element_by_xpath('//*[@id="dvPrintResult"]/a').click()
            driver.implicitly_wait(5)
            driver.switch_to.window(driver.window_handles[1])
            a = driver.find_elements_by_tag_name('span')
            try:
                row.append(a[-2].text)
                driver.close()
                row.append(link)
                driver.switch_to.window(driver.window_handles[0])
            except IndexError:
                driver.close()
                row.append('n/a')
                row.append(link)
                driver.switch_to.window(driver.window_handles[0])
        except NoSuchElementException:
            driver.implicitly_wait(17)
            driver.find_element_by_xpath('//*[@id="dvPrintResult"]/a').click()
            driver.implicitly_wait(5)
            driver.switch_to.window(driver.window_handles[1])
            a = driver.find_elements_by_tag_name('span')
            try:
                row.append(a[-2].text)
                driver.close()
                row.append(link)
                driver.switch_to.window(driver.window_handles[0])
            except IndexError:
                row.append('n/a')
                driver.close()
                row.append(link)
                driver.switch_to.window(driver.window_handles[0])
    except NoSuchElementException:
        row.append('n/a')
        row.append(link)
    df = pd.DataFrame({"Item Sold": (row[0::2]),"Link":(row[1::2])})
    print(df)
    df.to_csv('fill_in.csv')
