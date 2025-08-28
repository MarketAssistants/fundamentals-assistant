import json
import pandas as pd
import requests
from collections import deque
import time
from pathlib import Path
import os

headers = {"User-Agent": "yacineabc1997@gmail.com"}

def get_ciks(self):
    """Return dict mapping ticker -> zero-padded CIK.

    Looks for company_tickers.json relative to the project root (parent of this file's parent)
    or uses MA_COMPANY_TICKERS_JSON env var if provided.
    """
    project_root = Path(__file__).resolve().parents[1]  # MarketAssistants directory
    default_path = project_root / 'DATABASE' / 'company_tickers.json'
    json_path = Path(os.environ.get('MA_COMPANY_TICKERS_JSON', str(default_path)))
    if not json_path.is_file():
        raise FileNotFoundError(f"company_tickers.json not found at {json_path}. Set MA_COMPANY_TICKERS_JSON to override.")
    with json_path.open('r') as file:
        above_tojson = json.load(file)
    dictt = {above_tojson[key]["ticker"]: str(above_tojson[key]["cik_str"]).zfill(10) for key in above_tojson.keys()}
    return dictt

def get_company_fillings(cik): 
    filing_meta_data = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers )
    filings_json = filing_meta_data.json()

    all_forms = pd.DataFrame.from_dict(filings_json['filings']['recent'])

    return all_forms

def get_company_facts(self,cik): 

    company_facts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',headers=headers)
    facts_json = company_facts.json()
    
    #now it is like traversing a forest of dictionaries 
    # check .keys() to see the path ahead and direct yourself to the data you are looking for
    print("printing keys:")
    print(facts_json['facts'].keys())

    return facts_json['facts']['us-gaap']



def reformat_with_last_quarter_value(self,concept): 

    first_time_occurence = True 
    len_concept = len(concept)

    data_x = []
    data_y = []
    data_q = []
    valid = False
    counting = False
    skip_this_year = False
    counter = 0
    last_quarter = 0
    resultss_dic = {}
    for ixx,entry in enumerate(reversed(concept)):
        idx = len_concept - 1- ixx
        try: 
            last_frame =  entry['frame']
        except: 
            # print("skipped this entry: ",entry)
            if valid and ixx == len_concept-1: 
                return resultss_dic
            elif ixx == len_concept-1: 
                results_dic = {}       
                if len(data_x) != len(data_y): 
                    print(f"[ERROR]length of datax {len(data_x)} NOT MATCH length of datay {len(data_y)}")
                    for item in concept: 
                        if 'frame' in item.keys(): 
                            print(item)
                    return -1
                len_datay = len(data_y)
                for ii,dt in enumerate(reversed(data_x)): 
                    results_dic[dt] = data_y[len_datay-1-ii]

                return results_dic
            
            continue
        
        if valid or (len(last_frame) !=6 and len(last_frame) !=8): 
            #this means the json is already formatted well
            if not valid:
                print("ANNNOOOOOUUNCE: json is altready formatted")
                for item in concept: 
                    if 'frame' in item.keys(): 
                        print(item)
                print("reformating....")
            # print("continue ref....")
            valid = True
            resultss_dic[entry["end"]] = entry["val"]

            if ixx == len_concept-1: 
                return resultss_dic
            
            continue

        len_last_frame = len(last_frame)
        if len_last_frame == 6:  #if this is a year
            
            #deal with old stuff
            if first_time_occurence == False and not skip_this_year: 
                #check if 4 items are being assembled
                if last_quarter == 3: 
                    print("this must be a yearly thing...")
                    yeaar = last_frame[2:6]
                    data_x.append(entry['end'])
                    data_y.append(entry['val'])  
                    data_q.append(f'{yeaar}')
                    continue 

                elif last_quarter!=4 and last_quarter != 1: 
                    print(f"[ERROR]last quarter before entering the yearly metric is {last_quarter} NOT 1")
                    for item in concept: 
                        if 'frame' in item.keys(): 
                            print(item)
                    return adjust_output(concept,data_x,data_y)

                data_x[idx_to_be_replaced] = last_date
                data_y[idx_to_be_replaced] = last_yearly_value - counter

                if last_quarter ==4: 
                    skip_this_year = True
                else:
                    skip_this_year = False

            year_lookingat = last_frame[2:6]
            if not skip_this_year:
                last_date = entry['end']
                idx_to_be_replaced = len(data_x)
                last_yearly_value = entry['val']
                data_x.append(last_date)
                data_y.append(entry['val'])
                data_q.append(f'{year_lookingat}Q4')
            # else: 
            #     #check if any previous slots (error) that need to be resolved
            #     print("cleaning up error...")
            #     data_y = [data_y[i] for i in range(len(data_x)) if data_x[i] != 'error']
            #     data_x = [value for value in data_x if value != 'error']
            #start new stuff
            first_time_occurence = False
            counting = False
            last_quarter = 3
            counter = 0

        elif len_last_frame == 8: 

            if not first_time_occurence and last_quarter !=1: 
                year = last_frame[2:6]
                if year != year_lookingat:
                    print(f"[ERROR]--------------quarterly year {year} does not match year looking at : {year_lookingat}")
                    for item in concept: 
                        if 'frame' in item.keys(): 
                            print(item)
                    return adjust_output(concept,data_x,data_y)

            if counting : 
                previous_quarter = last_quarter
                last_quarter = int(last_frame[7])

                if last_quarter!=4 and last_quarter != (previous_quarter-1): 
                    print(f"ERROR] previous quarter {previous_quarter} / last quarter {last_quarter} MISMATCCCH")
                    for item in concept: 
                        if 'frame' in item.keys(): 
                            print(item)
                    return adjust_output(concept,data_x,data_y)

                if last_quarter!=4:
                    counter += entry['val']
                                
            else: 
                if not first_time_occurence and last_quarter != 3: 
                    print(f"[ERROR] last quarter when entering the quaterly metric is {last_quarter} NOT 3")
                    for item in concept: 
                        if 'frame' in item.keys(): 
                            print(item)
                    return adjust_output(concept,data_x,data_y)
                counter += entry['val']
                counting = True

            last_quarter = int(last_frame[7])
            year = last_frame[2:6]
            #append quarterly value for sure
            data_x.append(entry['end'])
            data_y.append(entry['val'])  
            data_q.append(f'{year}Q{last_quarter}')          

    return adjust_output(concept,data_x,data_y)

def adjust_output(concept,data_x,data_y):
    results_dic = {}       
    if len(data_x) != len(data_y): 
        print(f"[ERROR] length of datax {len(data_x)} NOT MATCH length of datay {len(data_y)}")
        for item in concept: 
            if 'frame' in item.keys(): 
                print(item)
        return -1    
    len_datay = len(data_y)
    # for ii,dt in enumerate(data_q): 
    #     results_dic[dt] = [data_y[ii],data_x[ii]]
    for ii,dt in enumerate(reversed(data_x)): 
        results_dic[dt] = data_y[len_datay-1-ii]

    return results_dic


def get_company_concept(self,cik, concept): 

    company_facts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',headers=headers)
    facts_json = company_facts.json()

    taxonomy_selected = "us-gaap" # default taxonomy
    for taxonomy in facts_json['facts'].keys(): 
        print("-------taxonomy: ",taxonomy)
        if concept in facts_json['facts'][taxonomy]: 
            taxonomy_selected = taxonomy
            print("===== taxonomy CHANGED: (else us-gaap) ", taxonomy_selected)
            break

    # a concept is for example: revenue
    company_concept = requests.get((f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'f'/{taxonomy_selected}/{concept}.json'),
    headers=headers)
    if company_concept.status_code < 200 or company_concept.status_code >= 300:
        print("concept response invalid")
        return None,-1,None

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
        print("========== key is: ",key)
        concept_df  = pd.DataFrame.from_dict(company_concept_json['units'][key])
        # print("full list of columns: ", concept_df.columns.tolist())
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None) 
        # print(concept_df)
        concept_df_json  = company_concept_json['units'][key]
        # print("concept json: ",concept_df_json)

        print("***** before reformating: ", concept_df_json)
        concept_json_reformated = reformat_with_last_quarter_value(self,concept_df_json)

        # print("********* reformated json: ", concept_json_reformated)
        return concept_json_reformated, 0,key

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







