import os 
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SansaarScraper():
# Scrapes the website using selenium in a variety of ways 
# -----------------------------------------------------------------------------------
# The scrape_today is a helper function returns a dataframe for today
# (all values are str), so use the pd converting functions to convert them to
# ints (pd.to_numeric). Scrape_today_by_range(sector, startDate) is an method to scrape
# all data upto a monthly range. 

    def __init__(self):
        self.url = 'https://www.sharesansar.com/today-share-price'
        self.driver = None 
        self.chrome_options = Options()
        self.chrome_options.add_argument('--window-size=1920,1080')  
      #  self.chrome_options.add_argument("--headless")

     
    def scrape_today(self, sector, date):
        findr = self.driver.find_element_by_xpath('//*[@id="fromdate"]')
        findr.click()
        findr.clear()
        findr.send_keys(date)
        self.driver.find_element_by_xpath('//*[@id="btn_todayshareprice_submit"]').click()
        time.sleep(2)
        dictionary_list = []

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        title_list = soup.find_all('th')
        for row in soup.find_all('tr'):
            dictionary_format = {}
            column = row.find_all('td')
            for i in range(len(column)):
                if i != 0:
                    dictionary_format[title_list[i].text]= column[i].text.replace('\n', '')
            if dictionary_format != {}:
                dictionary_list.append(dictionary_format)

        return pd.DataFrame(dictionary_list)

    # Let startDate be less than any number, OR enddate after testing is done 
    def scrape_today_by_range(self, sector, startDate):
        if self.driver == None:
            self.driver = webdriver.Chrome(options=self.chrome_options) 
        self.driver.get(self.url)
        
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="frm_todayshareprice"]/div[1]/span/span[1]/span'))).click()

        self.driver.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(sector)
        findr = self.driver.find_element_by_xpath('//*[@id="fromdate"]')
        findr.click()

        old_dates = self.driver.find_elements_by_css_selector('td.old')
        all_dates = self.driver.find_elements_by_css_selector('td.day')
        new_dates = self.driver.find_elements_by_css_selector('td.new')

        startdate = int(startDate[-2:])
        enddate = int([date for date in all_dates if date not in old_dates if date not in new_dates][-1].text)

        df_list = []
        date_list = []
        while startdate <= enddate:
            iter_date = startDate[:-2] + str(startdate)
            currDf = self.scrape_today(sector, iter_date)
            if not currDf.empty:
                df_list.append(currDf)
                date_list.append(iter_date)
            startdate += 1

        self.close_driver()
        return df_list, date_list

    
    def export_to_csv_range(self, sector, startdate):
        df_list, date_list = self.scrape_today_by_range(sector, startdate)
        directory = os.getcwd() + '/data/monthly/'
        fixed_str = sector.lower().strip().replace(' ', '')
        month = int(date_list[0][5:7])

        if month == 1:
            directory += 'january/'
        elif month == 2:
            directory += 'february/'
        elif month == 3:
            directory += 'march/'
        elif month == 4:
            directory += 'april/'
        elif month == 5:
            directory += 'may/'
        elif month == 6:
            directory += 'june/'
        elif month == 7:
            directory += 'july/'
        elif month == 8:
            directory += 'august/'
        elif month == 9:
            directory += 'september/'
        elif month == 10:
            directory += 'october/'
        elif month == 11:
            directory += 'november/'
        elif month == 12:
            directory += 'december/'

        if sector == 'All Sector':
            directory += 'allsector/'
        elif sector == 'Commercial Bank':
            directory += 'commercialbank/'
        elif sector == 'Development Bank':
            directory += 'developmentbank/'    
        elif sector == 'Finance':
            directory += 'finance/'
        elif sector == 'Hotel':
            directory += 'hotel/'
        elif sector == 'Hydropower':
            directory += 'hydropower/'
        elif sector == 'Life Insurance':
            directory += 'lifeinsurance/'
        elif sector == 'Manufacturing and Products':
            directory += 'manufacturingproducts/'
        elif sector == 'Microfinance':
            directory += 'microfinance/'
        elif sector == 'Mutual Fund':
            directory += 'mutualfund/'
        elif sector == 'Non-Life Insurance':
            directory += 'nonlifeinsurance/'
        elif sector == 'Others':
            directory += 'others/'
        elif sector == 'Promoter Share':
            directory += 'promotershare/'  
        elif sector == 'Trading':
            directory += 'trading/'     


        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(len(df_list)):
            df = df_list[i]
            dt = date_list[i]
            filename = directory + f'{fixed_str}_{dt}.csv'
            df.to_csv(filename)

    # Creates a master dataframe of whatever is inside the monthly directory 
    # Make sure that null dataframes are deleted. Divides master dataframe by rows
    # to make calculations easier. Make sure the month and you want to calculate 
    # for matches the directory names. 
    def month_stats(self, month, sector):
        directory = os.getcwd() + f'/data/monthly/{month}/{sector}/'
        df_list = []        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, index_col=0)
            if not df.empty:
                df_list.append(df)
        
        main_df = pd.concat(df_list, ignore_index=True).sort_values(by=['Symbol']).replace(',', '', regex=True)
        main_df.to_csv(os.getcwd() + f'/data/monthly/{month}/{sector}_{month}_master_df.csv')
        symbol_list = list(set(main_df['Symbol'].tolist()))

        dict_list = []
        for item in symbol_list:
            rows = main_df.loc[main_df['Symbol'] == item]
            values_dict = {
                'Symbol': item, 'AvgOpen.': rows['Open'].mean().round(2), 'AvgHigh': rows['High'].mean().round(2), 
                'AvgLow': rows['Low'].mean().round(2), 'AvgClose': rows['Close'].mean().round(2), 
                'AvgVol': pd.to_numeric(rows['Vol']).mean().round(2), 'AvgTransaction': pd.to_numeric(rows['Turnover']).mean().round(2),
                'AvgVWAP': rows['VWAP'].mean().round(2)
            }
            dict_list.append(values_dict)

        calculation_df = pd.DataFrame(dict_list)
        calculation_df.to_csv(os.getcwd() +  f'/data/monthly/{month}/{sector}_{month}_averages.csv')

    def calc_ranges(self, sector, startDate, endDate, rows):
        if self.driver == None:
            self.driver = webdriver.Chrome(options=self.chrome_options) 
        
        self.driver.get('https://www.sharesansar.com/index-history-data')
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="select2-sector-container"]'))).click()
        self.driver.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(sector)
        
        dp_start = self.driver.find_element_by_xpath('//*[@id="start"]')
        dp_start.click()
        dp_start.clear()
        dp_start.send_keys(startDate)

        dp_end = self.driver.find_element_by_xpath('//*[@id="end"]')
        dp_end.click()
        dp_end.clear()
        dp_end.send_keys(endDate)

        self.driver.find_element_by_xpath('//*[@id="select2-total_rows-container"]').click()
        self.driver.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(rows)
        self.driver.find_element_by_xpath('//*[@id="search1"]').click()

        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.close_driver()

        headers = soup.find_all('th')
        indices_list = []
        
        for i, row in enumerate(soup.find_all('tr')):
            if i != 0:
                indices_dict = {}
                column = row.find_all('td')
                for i in range(len(column)):
                    if i == 0 or i == 4 or i == 5:
                        indices_dict[headers[i].text] = column[i].text
                indices_list.append(indices_dict)
        
        indices_df = pd.DataFrame(indices_list).replace(',', '', regex=True)
        indices_df['AvgVolume.'] = pd.Series([pd.to_numeric(indices_df['Volume']).mean()]).round(2)
        start_close = float(indices_df.loc[indices_df['Date'] == startDate, 'Close'].values[0])
        end_close = float(indices_df.loc[indices_df['Date'] == endDate, 'Close'].values[0])
        indices_df['PercentInc.'] = pd.Series([((end_close-start_close)/start_close)*100]).round(2)

        indices_df.to_csv(os.getcwd() +  f'/data/{sector}_{startDate}_{endDate}_indices.csv')
        self.close_driver()

    def scrape_company_info(self, company):
        """
        Make sure to write the FULL name of the company for this to work, including the limiteds and such.
        It's because of how the scraping website has been structured. 
        """
        if self.driver == None:
            self.driver = webdriver.Chrome(options=self.chrome_options) 
        self.driver.get('https://www.sharesansar.com/')
        self.driver.find_element_by_xpath('//*[@id="companypagesearch"]').send_keys(company)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="eac-container-companypagesearch"]/ul/li[1]').click()
        # Latest divident information table
        dividend_table = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/section[2]/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/table/tbody'
        )

        dividend_soup = BeautifulSoup(dividend_table.get_attribute('innerHTML'), 'html.parser')
        # Gives the dividend information
        dividend_list = []
        for row in dividend_soup.find_all('tr'):
            info_type = None 
            val_type = None 
            for i, column in enumerate(row.find_all('td')):
                if i == 0:
                    info_type = column.text 
                elif i == 1:
                    val_type = column.text
            dividend_list.append({info_type:val_type})

        

 
    def close_driver(self):
        self.driver.close()

        




