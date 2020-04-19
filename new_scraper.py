import os 
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SansaarScraper():
# Scares the website using selenium in a variety of ways 
# -----------------------------------------------------------------------------------
# The scrape_today_by_sector returns a list of dictionaries (all values are str),
# so use the pd converting functions to convert them to ints (pd.to_numeric)
# scrape_today_by_range(sector, startDate) is an overloaded method to scrape
# all data upto a monthly range. 

    def __init__(self):
        self.url = 'https://www.sharesansar.com/today-share-price'
     
    def scrape_today_by_sector(self, sector, date):
        dictionary_list = []
        driver = webdriver.Chrome() 
        driver.get(self.url)

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="frm_todayshareprice"]/div[1]/span/span[1]/span'))).click()

        driver.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(sector)
        findr = driver.find_element_by_xpath('//*[@id="fromdate"]')
        findr.click()
        findr.clear()
        findr.send_keys(date)
        driver.find_element_by_xpath('//*[@id="btn_todayshareprice_submit"]').click()
        time.sleep(2)

        title_list = driver.find_elements_by_tag_name('th')
        row_list = driver.find_elements_by_tag_name('tr')
        row = 1
        while True:
            try:
                dictionary_format = {}
                driver.find_element_by_xpath(f'//*[@id="headFixed"]/tbody/tr[{row}]')
                column = 2
                while True:
                    try:
                        elem = driver.find_element_by_xpath(f'//*[@id="headFixed"]/tbody/tr[{row}]/td[{column}]')
                        dictionary_format[title_list[column-1].text] = elem.text
                        column += 1
                    except:
                        break 

                row += 1
                dictionary_list.append(dictionary_format)
            except:
                break 
        
        driver.close()
        return dictionary_list

    def scrape_today_by_range(self, sector, startDate):
        driver = webdriver.Chrome() 
        driver.get(self.url)

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="frm_todayshareprice"]/div[1]/span/span[1]/span'))).click()

        driver.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(sector)
        findr = driver.find_element_by_xpath('//*[@id="fromdate"]')
        findr.click()
        findr.clear()
        findr.send_keys(startDate)

        old_dates = driver.find_elements_by_css_selector('td.old')
        all_dates = driver.find_elements_by_css_selector('td.day')
        new_dates = driver.find_elements_by_css_selector('td.new')

        startdate = int(startDate[-2:])
        enddate = int([date for date in all_dates if date not in old_dates if date not in new_dates][-1].text)

        df_list = []
        while startdate <= 5:
            iter_date = startDate[:-2] + str(startdate)
            lister = self.scrape_today_by_sector(sector, iter_date)
            currDf = pd.DataFrame(lister)
            df_list.append(currDf)
            startdate += 1
        
        for df in df_list:
            print(df.head())
        return df_list


    def export_to_csv(self, sector, date):
        data = self.scrape_today_by_sector(sector, date)
        df = pd.DataFrame(data)
        directory = os.getcwd() + '/data_by_sector/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        todays_date = time.strftime('%Y%m%d')
        fixed_str = sector.lower().strip().replace(' ', '')
        filename = directory + f'{fixed_str}_{todays_date}.csv'
        df.to_csv(filename)

    def calculate_max_percent_increase_closing(self, sector, start_date, end_date):
    # This function assumes that the number of rows of records match completely in 
    # the date ranges, and it might not. Need to have checks for that or handle it 
    # somehow. It returns the percent increasing in closing prices.
        start_data = self.scrape_today_by_sector(sector, start_date)
        end_data = self.scrape_today_by_sector(sector, end_date)
        dfStart = pd.DataFrame(start_data)
        dfEnd = pd.DataFrame(end_data)

        start_close_col = pd.to_numeric(dfStart['Close'])
        end_close_col = pd.to_numeric(dfEnd['Close'])
        
        data = [
            dfStart['Symbol'], start_close_col, end_close_col, (end_close_col
            .sub(start_close_col)/start_close_col)*100
        ]

        max_percent_closing_df = pd.concat(
            data,
            axis=1,
            keys=['Symbol', 'StartClose', 'EndClose', 'PercentInClose']
        ).sort_values(by=['PercentInClose'], ascending=False)

        directory = os.getcwd() + '/data_by_sector/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        todays_date = time.strftime('%Y%m%d')
        fixed_str = sector.lower().strip().replace(' ', '')
        filename = directory + f'{fixed_str}-range_{start_date}_{end_date}.csv'
        max_percent_closing_df.to_csv(filename)
    
    def visualize(self):
        df = pd.read_csv(f'{os.getcwd()}' + '/data_by_sector/commercialbank_20200418.csv')
        close = df[df.columns[6]]
        prev_close = df[df.columns[9]]
        print(close)
        




