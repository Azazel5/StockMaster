import requests, bs4 
import xlsxwriter 
import sys 
from datetime import datetime
import os.path
from os import path
import psycopg2


destinationPath = "C:/Users/Sanjaya/Desktop/SummerInternshipGrind/pythonProgs/stockApp/stock_info_by_date_excel/stockPrices_"
todays_date = datetime.today().strftime("%Y-%m-%d")
destination = destinationPath + todays_date + ".xlsx"

if path.exists(destination):
    print("Today's stock prices have been saved already. Do it again tomorrow.")
    sys.exit(0)

conn = psycopg2.connect("dbname=Stock_Info user=postgres password=azazel_5")
cursor = conn.cursor()

url = 'http://www.nepalstock.com/todaysprice/export'
res = requests.get(url)
book = xlsxwriter.Workbook(destination)
bs4Request = bs4.BeautifulSoup(res.text, 'html.parser')
tdElements = bs4Request.select("td")
excelSheet = book.add_worksheet()
bold = book.add_format({'bold': True, 'align':'center'})

excelSheet.set_column(0, 0, 42)
excelSheet.set_column(1, 8, 18)

excelSheet.write("A1", "Traded Companies", bold)
excelSheet.write("B1", "Number Of Transactions", bold)
excelSheet.write("C1", "Max Price", bold)
excelSheet.write("D1", "Min Price", bold)
excelSheet.write("E1", "Closing Price", bold)
excelSheet.write("F1", "Traded Shares", bold)
excelSheet.write("G1", "Amount", bold)
excelSheet.write("H1", "Previous Closing", bold)
excelSheet.write("I1", "Difference Rs", bold)

row = 1
ids = 1

while len(tdElements) >= 8:
        stockList = []
        finaList = []
        excelSheet.write(row, 0, tdElements[0].contents[0])
        stockList.append(ids)
        finaList.append(ids)
        stockList.append(tdElements[0].contents[0])
        excelSheet.write(row, 1, float(tdElements[1].contents[0]))
        finaList.append(int(tdElements[1].contents[0]))
        excelSheet.write(row, 2, float(tdElements[2].contents[0]))
        finaList.append(float(tdElements[2].contents[0]))
        excelSheet.write(row, 3, float(tdElements[3].contents[0]))
        finaList.append(float(tdElements[3].contents[0]))
        excelSheet.write(row, 4, float(tdElements[4].contents[0]))
        finaList.append(float(tdElements[4].contents[0]))
        excelSheet.write(row, 5, float(tdElements[5].contents[0]))
        finaList.append(float(tdElements[5].contents[0]))
        excelSheet.write(row, 6, float(tdElements[6].contents[0]))
        finaList.append(float(tdElements[6].contents[0]))
        excelSheet.write(row, 7, float(tdElements[7].contents[0]))
        finaList.append(float(tdElements[7].contents[0]))
        excelSheet.write(row, 8, float(tdElements[8].contents[0]))
        finaList.append(float(tdElements[8].contents[0]))
        finaList.append(todays_date)
        stockTuple = tuple(stockList)
        finaTuple = tuple(finaList)
        ids += 1
        row += 1
        try:
            cursor.execute("""INSERT INTO stock (id, stock_name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING RETURNING id;""", stockTuple)
            id_getter = [stockTuple[0]]
            cursor.execute("SELECT date FROM financial_info WHERE stock_id = %s", tuple(id_getter))
            date_record = cursor.fetchone()
            if date_record == None or str(date_record[0]) != todays_date: 
                cursor.execute("""INSERT INTO financial_info (stock_id, number_of_transactions, max_price,
                                min_price, closing_price, traded_shares, amount, previous_closing,
                                difference_rs, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", finaTuple)
            else:
                print(stockTuple[1] + "'s information for " + todays_date + " has been added already!")

            conn.commit()
        except (Exception, psycopg2.Error) as error: 
            if conn:
                print("Failed to insert record, sorry!")
                print("Error is: " + str(error))
            else:
                print("We have no connection.")
        tdElements = tdElements[9:]
 
book.close()
if conn:
    conn.close() 
    cursor.close()


