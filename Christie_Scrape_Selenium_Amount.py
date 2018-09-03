import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome("C:\\Users\\Gabriel Hidalgo\\PycharmProjects\\scraper\\chromedriver.exe")

#Here I am using using the BS4 scraped table for the list of links of every auctions house   
a = pd.read_csv('All_Auction_House_Events.csv')

row = []

#Now, I am feeding that auction link list from BS4 Scrape to the Selenium Web craweler to collect the item number of
#the last art piece sold at each auction. Finally, I am placing all this into a CSV for later use when I am filling missing
#values that occured during this scrape.

for link in a['Link']:
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
    df.to_csv('Amount.csv')