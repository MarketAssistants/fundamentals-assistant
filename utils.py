import json
import pandas as pd
import requests
from collections import deque

headers = {"User-Agent": "yacineabc1997@gmail.com"}

def get_ciks():
    company_tickers = requests.get( "https://www.sec.gov/files/company_tickers.json" , headers=headers)
    above_tojson = company_tickers.json()
    
    dictt = {}
    for key in above_tojson.keys(): 
        dictt[above_tojson[key]["ticker"]] = str(above_tojson[key]["cik_str"]).zfill(10)
    return dictt

def get_company_fillings(cik): 
    filing_meta_data = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers )
    filings_json = filing_meta_data.json()

    all_forms = pd.DataFrame.from_dict(filings_json['filings']['recent'])

    return all_forms

def get_company_facts(cik): 

    company_facts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',headers=headers)
    facts_json = company_facts.json()
    
    #now it is like traversing a forest of dictionaries 
    # check .keys() to see the path ahead and direct yourself to the data you are looking for
    # print("printing keys:")
    # print(facts_json['facts'].keys())

    return facts_json['facts']['us-gaap']

def get_company_concept(cik, concept): 
    # a concept is for example: revenue
    company_concept = requests.get((f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'f'/us-gaap/{concept}.json'),
    headers=headers)
    if company_concept.status_code < 200 or company_concept.status_code >= 300:
        print("concept response invalid")
        return None,-1

    company_concept_json = company_concept.json()
    # print("concept keys:", company_concept_json.keys())
    concept_keys = company_concept_json['units'].keys()
    # if 'USD/shares' not in concept_keys: 
    #     print("Skipped-keys are: ",company_concept_json['units'].keys() )
    #     return None,-2
    # print("  ",company_concept_json['description'])
    # print(company_concept_json)
    # print("unit keys:", concept_keys)

    for key in concept_keys:
        concept_df  = pd.DataFrame.from_dict(company_concept_json['units'][key])
        # print("full list of columns: ", concept_df.columns.tolist())
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None) 
        # print(concept_df)
        concept_df_json  = company_concept_json['units'][key]
        # print("concept json: ",concept_df_json)
        return concept_df_json, 0

def test_only(ticker):
    ticker_cik_dict = get_ciks()
    cik = ticker_cik_dict[ticker]
    concept = get_company_concept(cik, "EarningsPerShareDiluted")
    print(concept)
    concept_10Q_only = concept[concept.form == '10-Q']

    last_eps = concept_10Q_only.iloc[-1]['val']
    print("last_eps is: ",last_eps)
     
    print(concept_10Q_only)
    trailing_4 = concept_10Q_only.tail(8)
    print(trailing_4)
    # concept_10Q_only.plot(x='end', y='val', kind='line')
    # plt.title('Line Plot of DataFrame')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()

def get_trailing_eps(concept): 
    nbr_trailing = 4
    
    last_frame= concept.iloc[-1]['frame']
    len_last_frame = len(last_frame)

    if len_last_frame == 6: 
        return concept.iloc[-1]['val']
    else: 
        year = int(last_frame[2:6])
        quarter = int(last_frame[7])
        condition = f"CY{year}Q{quarter}"

    reversed_df = concept.iloc[::-1]

    trailing_eps =0
    yearly = False
    year_counter = 4
    for index, row in reversed_df.iterrows():

        if yearly: 
            if year_counter == 4 and row['frame'] == condition:
                year_value = row['val']
                year_counter -=1
                condition = f"CY{year}Q{quarter}"
                nbr_trailing -=1

            elif row['frame'] == condition: 
                if nbr_trailing !=0: 
                    trailing_eps += row['val']
                    nbr_trailing -=1
                quarter -=1
                condition = f"CY{year}Q{quarter}"
                year_value -= row['val']
                year_counter -=1
                if year_counter ==0: 
                    trailing_eps += year_value
                    return round(trailing_eps,2)

        elif row['frame'] == condition: 

            #3-add-2-add-1-add-0--add
            nbr_trailing -=1
            #add it
            trailing_eps += row['val']
            #check if we collected the needed quarters
            if nbr_trailing ==0:
                return trailing_eps

            if quarter == 1: 
                quarter =3
                year -=1
                condition = f"CY{year}"
                yearly = True
            else:
                quarter -=1
                condition=f"CY{year}Q{quarter}"



def get_trailing_eps_bytree (data): 
#date is a data_frame

    list_accepted_forms = ['10-Q', '10-K', '10-Q/A', '10-K/A']
    disqualified = [] # this will be a list of lists (each list is for a level)
    visited_queue = deque() #this is a lifo queo (append() to add, pop() to pop)
    current_level =0 
    for index, row in data: 

        if row['form'] in  list_accepted_forms: 
            
            most_recent_day = row['start'] 




        

                
        