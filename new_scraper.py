import os 
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        self.driver = webdriver.Chrome() 
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
            df_list.append(currDf)
            date_list.append(iter_date)
            startdate += 1

        self.driver.close()
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

        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(len(df_list)):
            df = df_list[i]
            dt = date_list[i]
            filename = directory + f'{fixed_str}_{dt}.csv'
            df.to_csv(filename)

    # Creates a master dataframe of whatever is inside the monthly directory 
    # Make sure that null dataframes are deleted. Divides master dataframe by rows
    # to make calculations easier
    def calculations(self):
        directory = os.getcwd() + '/data/monthly/january/'
        df_list = []        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, index_col=0)
            if not df.empty:
                df_list.append(df)
        
        main_df = pd.concat(df_list, ignore_index=True).sort_values(by=['Symbol']).replace(',', '', regex=True)
        main_df.to_csv(os.getcwd() + '/data/monthly/master_df.csv')
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
        calculation_df.to_csv(os.getcwd() + '/data/monthly/calculations.csv')


        """
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

        directory = os.getcwd() + '/data/range/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        todays_date = time.strftime('%Y%m%d')
        fixed_str = sector.lower().strip().replace(' ', '')
        filename = directory + f'{fixed_str}-range.csv'
        max_percent_closing_df.to_csv(filename)
    """

    
    def visualize(self):
        df = pd.read_csv(f'{os.getcwd()}' + '/data/commercialbank_20200418.csv')
        close = df[df.columns[6]]
        prev_close = df[df.columns[9]]
        print(close)




        




