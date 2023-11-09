
import pandas as pd 
import yfinance as yf

def get_filtered_list(self,):
    df_t = pd.read_csv('nasdaq_screener.csv')
    desired_market_cap = 1000000000  # Replace with your desired market cap value
    tickers = df_t.loc[df_t['Market Cap'] >= desired_market_cap, 'Symbol'].tolist()

    #sister companies in the reasearch (for comparison  purposes)
    specific_companies = []

    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)
        try: 
            country = ticker.info['country']
            sector_desc = ticker.info['industryDisp']
            description = ticker.info['longBusinessSummary']

        except: 
            continue 

        desc_lower = description.lower()
        if  country == 'United States' and ("cloud " in desc_lower  or "cloud-related" in desc_lower) and (sector_desc == "Software—Infrastructure" or sector_desc == "Software—Application") : 
            specific_companies.append(ticker_symbol)

    return specific_companies