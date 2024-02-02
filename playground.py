
# import urllib.request

# xml_url = "https://www.sec.gov/Archives/edgar/data/12927/000122520824000416/xslF345X05/doc4.xml"
# destination_file = "downloaded_file.xml"

# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
# req = urllib.request.Request(xml_url, headers=headers)

# # Use urlopen to open the URL and read its content
# with urllib.request.urlopen(req) as response:
#     xml_content = response.read()

# # Save the content to a file
# with open(destination_file, 'wb') as file:
#     file.write(xml_content)

# print(f"The XML file has been downloaded and saved as {destination_file}")


# import json
# import pandas as pd
# import requests
# from collections import deque

# concept = 'Revenues'
# cik="0001759509"
# headers = {"User-Agent": "yacineabc1997@gmail.com"}
# company_facts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',headers=headers)
# facts_json = company_facts.json()

# taxonomy_selected = "us-gaap" # default taxonomy
# for taxonomy in facts_json['facts'].keys(): 
#     print("-------taxonomy: ",taxonomy)
#     if concept in facts_json['facts'][taxonomy]: 
#         taxonomy_selected = taxonomy
#         print("===== taxonomy CHANGED: (else us-gaap) ", taxonomy_selected)
#         break

# company_concept = requests.get((f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'f'/{taxonomy_selected}/{concept}.json'),
# headers=headers)
# if company_concept.status_code < 200 or company_concept.status_code >= 300:
#     print("concept response invalid")
#     exit(0)

# company_concept_json = company_concept.json()
# # print("concept keys:", company_concept_json.keys())
# concept_keys = company_concept_json['units'].keys()
# # if 'USD/shares' not in concept_keys: 
# #     print("Skipped-keys are: ",company_concept_json['units'].keys() )
# #     return None,-2
# # print("  ",company_concept_json['description'])
# # print(company_concept_json)
# # print("unit keys:", concept_keys)

# for key in concept_keys:
#     print("========== key is: ",key)
#     concept_df  = pd.DataFrame.from_dict(company_concept_json['units'][key])
#     # print("full list of columns: ", concept_df.columns.tolist())
#     # pd.set_option('display.max_columns', None)
#     # pd.set_option('display.max_rows', None) 
#     # print(concept_df)
#     concept_df_json  = company_concept_json['units'][key]
#     # print("concept json: ",concept_df_json)
#     print( concept_df_json, 0,key)




# from yahoo_fin.stock_info import *


# print(get_analysts_info('tgt')['Earnings History'])

# print(get_earnings_history('tgt'))

# import pandas as pd
# from io import StringIO
# def tickers_sp500(include_company_data = False):
#     '''Downloads list of tickers currently listed in the S&P 500 '''
#     # get list of all S&P 500 stocks
#     sp500 = pd.read_html(StringIO("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"))[0]
#     sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=True)

#     if include_company_data:
#         return sp500

#     sp_tickers = sp500.Symbol.tolist()
#     sp_tickers = sorted(sp_tickers)
    
#     return sp_tickers

# print(tickers_sp500())

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # URL of the Wikipedia page
# url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# # Send a GET request to fetch the page content
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.content, "html.parser")
    
#     # Find the table containing the S&P 500 company data
#     table = soup.find("table", {"class": "wikitable"})

#     # Read the table using pandas
#     if table:
#         df = pd.read_html(str(table))[0]  # Convert the table to a DataFrame
#         print(df)  # Display the first few rows of the DataFrame
#     else:
#         print("Table not found on the page.")
# else:
#     print("Failed to fetch the page.")

# import yfinance as yf
# msft = yf.Ticker("MSFT")
# print(msft.info)
# from finvizfinance.news import News
# fnews = News()
# all_news = fnews.get_news()
# print(all_news['news'].head())
# print(all_news)

# from yahoo_earnings_calendar import YahooEarningsCalendar
# import datetime

# yec = YahooEarningsCalendar()
#     # Returns a list of all available earnings of BOX
# first_date = datetime.date(2023, 6, 30)
# last_date = datetime.date(2023, 8, 30)
# print(yec.earnings_between(first_date, last_date))

# from yahoofinance import AssetProfile
# req = AssetProfile('AAPL')
# import numpy as np
# import matplotlib.pyplot as plt

# data = np.array([10, 15, 20, 22, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70])
# num_bins = int(np.ceil(np.log2(len(data)) + 1))

# hist_values, bin_edges = np.histogram(data, bins=num_bins)
 
# plt.hist(data, bins=num_bins, edgecolor='k', alpha=0.7)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Continuous Frequency Distribution')
# plt.grid(True)
# plt.show()

# # import numpy as np
# # import plotly.express as px
# # import pandas as pd

# # # Sample data
# # data = np.array([10, 15, 20, 22, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70])

# # # Determine the number of bins
# # num_bins = int(np.ceil(np.log2(len(data)) + 1))

# # # Create a histogram
# # hist_values, bin_edges = np.histogram(data, bins=num_bins)

# # # Create a DataFrame for Plotly
# # df = pd.DataFrame({'Value': bin_edges[:-1], 'Frequency': hist_values})

# # # Create an interactive histogram using Plotly
# # fig = px.bar(df, x='Value', y='Frequency', title='Interactive Continuous Frequency Distribution')

# # # Customize the appearance
# # fig.update_traces(marker_color='royalblue', opacity=0.7)
# # fig.update_xaxes(title_text='Value')
# # fig.update_yaxes(title_text='Frequency')
# # fig.update_layout(bargap=0.05)
# # fig.update_layout(showlegend=False)

# # # Show the interactive plot
# # fig.show()


# a = ['a', 'b', 'c']
# b = a
# b.remove('a')
# print(a)
# print(b)

# ordered_ratios;
# [34.858069832869404, 62.793969769849845, 72.27714071468431, 119.64796942633552, 139.43227933147762, 160.9809043190696, 186.39894184313323, 205.90580784997275, 210.80832708449591, 347.2137151979933, 571.2225637128277, 590.2633158365886, 632.4249812534877, 655.8481287073206, 1041.6411455939797, 1180.5266316731772, 1362.1461134690505, 1362.1461134690505, 4426.974868774414, 4426.974868774414, 5902.633158365886, 8853.949737548828, 17707.899475097656]
# ordered concepts: 
# [5.08, 2.82, 2.45, 1.48, 1.27, 1.1, 0.95, 0.86, 0.84, 0.51, 0.31, 0.3, 0.28, 0.27, 0.17, 0.15, 0.13, 0.13, 0.04, 0.04, 0.03, 0.02, 0.01]
# ['DOCN', 'CDAY', 'CRWD', 'BOX', 'BLKB', 'DT', 'CALX', 'ATEN', 'TDC', 'PRGS', 
#  'CVLT', 'WDAY', 'PANW', 'PTC', 'AKAM', 'ORCL', 'QLYS', 'VMW', 'PLUS', 'FFIV', 'MSFT', 'ADBE', 'NOW']

report = "getall:jkmmm,lsjh,wear,ioi"
elements = report.split(':')[1]
list_reports = elements.split(',')
print(list_reports)