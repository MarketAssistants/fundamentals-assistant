import yfinance as yf
import pandas as pd
from tqdm import tqdm

def get_filtered_list():
    df_t = pd.read_csv('nasdaq_screener.csv')
    desired_market_cap = 1000000000  # Replace with your desired market cap value
    tickers = df_t.loc[df_t['Market Cap'] >= desired_market_cap, 'Symbol'].tolist()
    nbr_tickers = len(tickers)

    specific_companies =[]


    tickers = ['AAPL', 'ACIW', 'ACN', 'ADBE', 'ADP', 'ADSK', 'AGYS', 'AIU', 'AKAM', 'ALGN', 'ALIT', 'ALKT', 'ALRM', 'ALTR', 'AMD', 'ANET', 'ANSS', 'APPF', 'ARLO', 'ARW', 'ASGN', 'ATEN', 'AVID', 'AVPT', 'AXON', 'AYX', 'BABA', 'BBUC', 'BIDU', 'BILL', 'BL', 'BLKB', 'BMI', 'BOX', 'BR', 'BRZE', 'CABO', 'CACI', 'CALX', 'CCCS', 'CD', 'CDAY', 'CDW', 'CFLT', 'CHH', 'CHKP', 'CHT', 'CIG', 'CLBT', 'CLS', 'COMP', 'CRM', 'CRWD', 'CSCO', 'CVLT', 'CXM', 'CYBR', 'DAVA', 'DCBO', 'DDOG', 'DFIN', 'DGII', 'DOCN', 'DOCS', 'DOX', 'DSGX', 'DT', 'DXC', 'ENPH', 'ERIC', 'ESMT', 'ESTC', 'ETWO', 'EXPI', 'EXTR', 'FFIV', 'FI', 'FIVN', 'FLEX', 'FORTY', 'FOUR', 'FRSH', 'FSLY', 'GD', 'GDDY', 'GDS', 'GLOB', 'GOOG', 'GOOGL', 'GWRE', 'HAL', 'HCP', 'HLIT', 'HON', 'HPE', 'HQY', 'HUBS', 'IAS', 'IBM', 'INFA', 'INST', 'INTA', 'INTC', 'INTU', 'IONQ', 'IOT', 'IQV', 'IRTC', 'ITRI', 'JAMF', 'JBL', 'JNPR', 'KC', 'KD', 'KT', 'LBTYA', 'LBTYB', 'LBTYK', 'LDOS', 'LEA', 'LSPD', 'LUMN', 'MANH', 'MBLY', 'MDB', 'MDRX', 'MLNK', 'MNDY', 'MODN', 'MQ', 'MSFT', 'MSTR', 'MU', 'NABL', 'NBR', 'NCNO', 'NCR', 'NET', 'NEWR', 'NICE', 'NOK', 'NOW', 'NSIT', 'NSP', 'NTAP', 'NTCT', 'NTES', 'NTNX', 'NTRA', 'NVDA', 'OKTA', 'OLK', 'ORAN', 'ORCL', 'OTEX', 'PANW', 'PAR', 'PAY', 'PAYC', 'PAYX', 'PCOR', 'PCTY', 'PEGA', 'PI', 'PLUS', 'PRFT', 'PRGS', 'PSTG', 'PTC', 'PWSC', 'PYCR', 'QCOM', 'QLYS', 'QTWO', 'RBLX', 'RCI', 'REZI', 'RILY', 'RMD', 'RNG', 'ROP', 'RPD', 'S', 'SAIC', 'SANM', 'SAP', 'SEDG', 'SGH', 'SKM', 'SMCI', 'SNOW', 'SNX', 'SOFI', 'SOS', 'SPLK', 'SPSC', 'SPT', 'STER', 'STGW', 'STX', 'SWI', 'T', 'TDC', 'TDS', 'TEAM', 'TEF', 'TENB', 'TER', 'TIGO', 'TIXT', 'TKC', 'TOST', 'TTD', 'TTWO', 'TU', 'TWKS', 'TWLO', 'TYL', 'UPST', 'VEEV', 'VERX', 'VIAV', 'VIV', 'VMW', 'VOD', 'VRNS', 'VRNT', 'WDAY', 'WIT', 'WIX', 'WK', 'XYL', 'ZBRA', 'ZD', 'ZETA', 'ZI', 'ZM', 'ZS', 'ZUO']
    tickers_secondrun = ['ADBE', 'AGYS', 'AKAM', 'ALRM', 'ALTR', 'APPF', 'ATEN', 'AVPT', 'BLKB', 'BOX', 'BRZE', 'CALX', 'CDAY', 'CRWD', 'CVLT', 'CXM', 'DDOG', 'DOCN', 'DOX', 'DT', 'FFIV', 'FIVN', 'FSLY', 'GWRE', 'HCP', 'IOT', 'JAMF', 'MDB', 'MODN', 'MSFT', 'MSTR', 'NET', 'NOW', 'NTCT', 'NTNX', 'OKTA', 'ORCL', 'PANW', 'PAR', 'PEGA', 'PLUS', 'PRGS', 'PTC', 'QLYS', 'QTWO', 'RNG', 'RPD', 'S', 'SPLK', 'SPT', 'SWI', 'TDC', 'TENB', 'TYL', 'VERX', 'VMW', 'VRNS', 'VRNT', 'WDAY', 'WK', 'ZETA', 'ZM', 'ZS']
    tickers_omitted= ['AGYS', 'ALRM', 'CXM', 'GWRE', 'IOT', 'MODN', 'MSTR', 'PAR', 'TYL', 'VERX', 'ZETA', 'ZM', 'ZS'] 

    tickers_final =  [item for item in tickers_secondrun if item not in tickers_omitted]


    if RETURN_FINAL_LIST:
     return tickers_final
        
    num_tickers = len(tickers_secondrun)
    print("number of tickers to begin with: ", num_tickers)
    print("number of tickers to be omitted is: ", len(tickers_omitted))

    # tickers_exp = ['DDOG']
    progress_bar = tqdm(total= num_tickers, desc="overall")

    if JUST_TOP: 
        exit(0)

    for ticker_symbol in tickers_secondrun:
        # print("checking: ", ticker_symbol, end=".")
        print("ticker-------", ticker_symbol)
            # Create a Ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # if ticker_symbol == 'AAPL':
        #     print(ticker.info.keys())
        #     break

        try: 

            # print("industry: ", end='' )
            # print(ticker.info['industry'])
            # print("industryDisp: ", end='' )
            # print(ticker.info['industryDisp'])
            # print("sector: ", end='' )
            # print(ticker.info['sector'])
            # print("sectorDisp: ", end='' )
            # print(ticker.info['sectorDisp'])

                
            country = ticker.info['country']
            sector_desc = ticker.info['industryDisp']
            description = ticker.info['longBusinessSummary']

            if PRINT_DESC: 
                print(sector_desc + " "+description)
        except: 
            progress_bar.update(1)
            continue 

            # Print the description
        # print("Ticker Symbol:", ticker_symbol)
        # print("Company Description:")
        # print(description)
        # print(type(description))

        if RUN_ANALYSIS:
            desc_lower = description.lower()
            if  country == 'United States' and ("cloud " in desc_lower  or "cloud-related" in desc_lower) and (sector_desc == "Software—Infrastructure" or sector_desc == "Software—Application") : 
                specific_companies.append(ticker_symbol)
                print("======added!")

            progress_bar.update(1)

    progress_bar.close()

    if RUN_ANALYSIS:
        print(specific_companies)
        print("number of companies filtered now is: ", len(specific_companies))
