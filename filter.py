import yfinance as yf
import pandas as pd
from tqdm import tqdm

df_t = pd.read_csv('nasdaq_screener.csv')
desired_market_cap = 1000000000  # Replace with your desired market cap value
tickers = df_t.loc[df_t['Market Cap'] >= desired_market_cap, 'Symbol'].tolist()
nbr_tickers = len(tickers)

specific_companies =[]

progress_bar = tqdm(total= nbr_tickers, desc="overall")
for ticker_symbol in tickers:
    print("checking: ", ticker_symbol, end=".")
        # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # print(ticker.info.keys())
    # print(ticker.info)
        # Get the company's description
    try: 
        description = ticker.info['longBusinessSummary']
    except: 
        progress_bar.update(1)
        continue 

        # Print the description
    # print("Ticker Symbol:", ticker_symbol)
    # print("Company Description:")
    # print(description)
    # print(type(description))

    desc_lower = description.lower()

    if "cloud" in desc_lower: 
        specific_companies.append(ticker_symbol)

    progress_bar.update(1)

progress_bar.close()
print(specific_companies)

