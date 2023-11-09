import numpy as np 
import math
import yfinance as yf
import requests
from tqdm import tqdm
import pandas as pd 
import json
import matplotlib.pyplot as plt
import pprint
from fundamentals_assistant.extra import get_filtered_list
from plot import plot_histogram, plot_xy
from copy import deepcopy
from timing import tomorrow_date, today_date,last_business_day
from utils import get_ciks, get_company_fillings, get_company_facts, get_company_concept,test_only, get_trailing_eps

class Fundamentals_Assistant: 


    def __init__(self): 
        #Change these operational variables
        self.TESTING_ONLY = False
        self.PRINT_HISTOGRAM_ALL = False
        self.PRINT_HISTOGRAM_POSITIVES = False

        self.DO_POST_GRAPHING_ANALYSIS =False
        self.PRINT_REWARD_GRAPH = True 


def get_eps(types_list):
    ticker_cik_dict = get_ciks()
    # print("got here!")
    new_list, ratio_data, concept_data = [],[],[]
    new_list_pos, ratio_data_pos, concept_data_pos = [],[],[]
    nbr_invalids =0 
    nbr_neg_ratios = 0
    cntr =0

    invalids =[]
    nbr_invalid_concept_requests = 0
    nbr_invalid_concept_key = 0


    cik = ticker_cik_dict[ticker]

    # company_fillings= get_company_fillings(cik)
    # simplified_fillings = company_fillings[['accessionNumber', 'reportDate', 'form']].head(50)

    # most_recent_filling  = simplified_fillings

    # company_facts_usgaap = get_company_facts(cik)
    # list_facts = company_facts_usgaap.keys()

    # pp = pprint.PrettyPrinter()
    # pp.pprint(list_facts)
    #each fact (ex. Revenue, Assets) contains several entries as dictionary with filling date and form filed as some of the keys. 
    concept, response = get_company_concept(cik, "EarningsPerShareDiluted")
    if response !=0:  
        if response == -1: 
            nbr_invalid_concept_requests +=1
        elif response ==-2: 
            nbr_invalid_concept_key +=1

    # # filter the data
    # concept.form == '10-Q'
    # concept_10Q_only = concept
    concept['form'] = concept['form'].astype(str)
    concept_10Q_only = concept[concept.form.isin(['10-Q', '10-K', '10-Q/A', '10-K/A']) ]
    # if ticker != "CVLT":
    concept_10Q_only= concept_10Q_only.dropna(how='any')
    concept_10Q_only = concept_10Q_only.reset_index(drop=True)
    
    if concept_10Q_only.empty: 
        nbr_invalids+=1
        cntr+=1

    results = tuple(None for _ in range(len(types_list)))

    for idx,type in enumerate(types_list): 
        if type == "last": 
            res = concept_10Q_only.iloc[-1]['val']
        elif type == "trailing": 
            res = get_trailing_eps(concept)
        results[idx] = res
            
    reversed_df = concept_10Q_only.iloc[::-1]

    counter = 0
    sett = set()
    frame_skip=False
    for index, row in reversed_df.iterrows():
        # print(row["frame"])
        if "frame" not in row: 
            print ("=======>ERROR: FRAME COLUMN DOES NOT EXIST!!!!")
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(concept_10Q_only.to_string(index=False))
            frame_skip = True
            break

        if frame_skip: 
            frame_skip=False
            continue

        sett.add(row["frame"])
        counter +=1 


    if len(sett) != 4: 
        print("----working on: ", ticker)
        print ("=======>ERROR: NON_CONTINGET!!!!")
        print(sett)

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(concept_10Q_only.to_string(index=False))

        continue

    years_cntr, quarter_cntr, invalid_cntr = 0,0,0
    for frame in sett: 
        if len(frame) == 6: 
            years_cntr +=1
        elif len(frame) == 8: 
            quarter_cntr +=1
        else: 
            invalid_cntr +=1

    if years_cntr ==1 and quarter_cntr == (4-years_cntr) and invalid_cntr ==0: 

        continue    
    else:
        print("----working on: ", ticker)
        print ("=======>ERROR: NON_CONTINGET!!!!")
        print("years_cntr: ",years_cntr)
        print("quarter_cntr: ",quarter_cntr)
        print("invalid_cntr: ",invalid_cntr)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(concept.to_string(index=False))
        continue

    # if ticker == 'CVLT':
    #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #         print(concept_10Q_only.to_string(index=False))


    if trailing_yearly_eps is None:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(concept_10Q_only.to_string(index=False))

    # print("trailing eps: ", trailing_yearly_eps)
    
    # print(concept_10Q_only)  
    # exit(0)  
    # if last_eps < 0: 
    #     nbr_neg_ratios+=1
    try:
        data_test = yf.download(ticker, start=last_business_day(), end=tomorrow_date(), progress=False)
        price = data_test[['Close']].iloc[0, 0]
        # print(price)
    except: 
        nbr_invalids +=1
        cntr+=1
        progress_bar.update(1)
        continue
    
    concept_data.append(last_eps)
    addition= 0 if last_eps==0 else price/last_eps
    ratio_data.append(addition)
    new_list.append(ticker)
    
    if last_eps>0: 
        concept_data_pos.append(last_eps)
        ratio_data_pos.append(price/last_eps)
        new_list_pos.append(ticker)
    cntr +=1
    # print(concept_10Q_only)
    # #try plotting
    # concept_10Q_only.plot(x='end', y='val', kind='line')
    # plt.title('Line Plot of DataFrame')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()

    #find histograms of price/eps valuation of companies belonging to a field or domain.
    #put it alongsie the eps histogram and study the situation. 

    #or instead of using your eyes to study the situation go over your thought process and replicate that in the form of 
    #code, every thought process during the comparison or filtration is a step in the algorithm. Our brains solve problems, find optimal solutions 
    #through a series of comparasion reward sytem
    progress_bar.update(1)

progress_bar.close()

# print("ratios: ",ratio_data )
# print("number of negatives", nbr_neg_ratios)
print("\033[1m","number of valid companies (included in histogram): ",len_filtered_list- nbr_invalids,"\033[0m")
print("\033[1m","number of invalids (ex. no 10Q): ", nbr_invalids,"\033[0m")

#we have ratio data pos: all valid ratios (non empty sec, available last price)
#we have concept data pos: all valid eps (non empty sec, available last price)
#we have new list pos:list of tickers maching valid data (non empty sec, available last price)

ratio_data_all_np = np.array(ratio_data, dtype="float")
ratio_data_np = np.array(ratio_data_pos, dtype="float")
concept_data_np = np.array(concept_data_pos, dtype="float")

FLAGS = [PRINT_HISTOGRAM_ALL, PRINT_HISTOGRAM_POSITIVES]

plot_histogram(ratio_data_all_np, ratio_data_np, "P/E last quarter", FLAGS)


if not DO_POST_GRAPHING_ANALYSIS: 
    print("no post analysis requested")
    exit(0)

ordered_ratio_idx = np.argsort(ratio_data_np)
ordered_ratio = [ratio_data_np[index] for index in ordered_ratio_idx]
ordered_ticker_list = [new_list_pos[index] for index in ordered_ratio_idx]
ordered_concept_data = [concept_data_np[index] for index in ordered_ratio_idx]
order_length = len(ordered_concept_data)
reward = np.zeros(order_length)

#for testing
# print("ordered ratios: ")
# print(ordered_ratio)
# print("ordered_concepts: ")
# print(ordered_concept_data)
# print("ordered_corresponding ticker list:")
# print(ordered_ticker_list)


for cntr,concept in enumerate(ordered_concept_data): 
    for cntr_2 in range(cntr+1,order_length): 
        if concept >= ordered_concept_data[cntr_2]: 
            reward[cntr] +=1

# print("reward list is: ")
# print(reward)

if PRINT_REWARD_GRAPH:
    plot_xy(reward)

results_idx = np.argsort(-reward)
# print("results_idx is: ")
# print(results_idx)
winner_tickers = [ordered_ticker_list[index] for index in results_idx]
reward_winnners = np.array([reward[index] for index in results_idx])
ratio_winnners = np.array([ordered_ratio[index] for index in results_idx], dtype="float")
concept_winners= np.array([ordered_concept_data[index] for index in results_idx], dtype="float")

# print("ratio winners are: ", ratio_winnners)
# print("concept_winners are: ", -concept_winners)
ratio_indices = np.argsort(ratio_winnners)
# print("ratio indices: ", ratio_indices)
concept_indices = np.argsort(-1*concept_winners)
# print("concept indices: ", concept_indices)

ratio_ranks = np.zeros(order_length)
concept_ranks = np.zeros(order_length)

rank =1
for ratio_idx, concept_idx in zip(ratio_indices,concept_indices): 
    # print("adding to concept index: ", results_idx[concept_idx])
    # print("adding to ratio index: ", results_idx[ratio_idx])
    concept_ranks[concept_idx] = rank
    ratio_ranks[ratio_idx] = rank
    rank+=1

for rank,ticker in enumerate(winner_tickers): 
    print(f"{rank+1} - {ticker}: reward:{reward_winnners[rank]} ratio(rk. {ratio_ranks[rank]}): {ratio_winnners[rank]} eps(rk. {concept_ranks[rank]}): {concept_winners[rank]}")
