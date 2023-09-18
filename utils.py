import json
import pandas as pd
import requests

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

    return facts_json['facts']['us-gaap']

def get_company_concept(cik, concept): 
    # a concept is for example: revenue
    company_concept = requests.get((f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'f'/us-gaap/{concept}.json'),
    headers=headers)
    company_concept_json = company_concept.json()

    concept_df  = pd.DataFrame.from_dict(company_concept_json['units']['USD'])

    return concept_df


