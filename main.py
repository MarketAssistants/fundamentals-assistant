import numpy as np 
import yfinance as yf
import requests
import pandas as pd 
import json
import matplotlib.pyplot as plt
import pprint
from filter import get_filtered_list
from plot import plot_histogram, plot_xy


from copy import deepcopy
from timing import tomorrow_date, today_date

from utils import get_ciks, get_company_fillings, get_company_facts, get_company_concept,test_only

TESTING_ONLY = True


if TESTING_ONLY==True: 
    ticker = 'NOW'
    test_only(ticker)
    exit(0)


ticker_cik_dict = get_ciks()
# print("got here!")

filtered_list = get_filtered_list()

new_list, ratio_data, concept_data = [],[],[]
new_list_pos, ratio_data_pos, concept_data_pos = [],[],[]
nbr_invalids =0 
nbr_neg_ratios = 0
cntr =0

invalids =[]
for ticker in filtered_list:
    print("----working on: ", ticker)
    cik = ticker_cik_dict[ticker]
    # company_fillings= get_company_fillings(cik)
    # simplified_fillings = company_fillings[['accessionNumber', 'reportDate', 'form']].head(50)

    # most_recent_filling  = simplified_fillings

    # company_facts_usgaap = get_company_facts(cik)
    # list_facts = company_facts_usgaap.keys()

    # pp = pprint.PrettyPrinter()
    # pp.pprint(list_facts)
    #each fact (ex. Revenue, Assets) contains several entries as dictionary with filling date and form filed as some of the keys. 
    concept = get_company_concept(cik, "EarningsPerShareDiluted")
    # print("forms in the concept", concept.form)

    # break

    # #check structure
    # # print(concept.columns)
    # # print(concept.form)

    # # filter the data
    concept_10Q_only = concept[concept.form == '10-Q']
    if concept_10Q_only.empty: 
        nbr_invalids+=1
        cntr+=1
        continue
    # #drops the original index (first column) makes new indexes incrementing due to filtered data only (no gaps)
    # concept_10Q_only = concept_10Q_only.reset_index(drop=True)

    last_eps = concept_10Q_only.iloc[-1]['val']
    
    # if last_eps < 0: 
    #     nbr_neg_ratios+=1

    try:
        data_test = yf.download('AAPL', start=today_date(), end=tomorrow_date(), progress=False)
        price = data_test[['High']].iloc[0, 0]
    except: 
        nbr_invalids +=1
        cntr+=1
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

    # EarningsPerShareDiluted


    #find histograms of price/eps valuation of companies belonging to a field or domain.
    #put it alongsie the eps histogram and study the situation. 

    #or instead of using your eyes to study the situation go over your thought process and replicate that in the form of 
    #code, every thought process during the comparison or filtration is a step in the algorithm. Our brains solve problems, find optimal solutions 
    #through a series of comparasion reward sytem

# print("ratios: ",ratio_data )
# print("number of negatives", nbr_neg_ratios)
print("number of invalid (ex. no 10Q)", nbr_invalids)

# plot_histogram(ratio_data, "P/E last quarter")

#we have ratio data pos: all valid ratios (non empty sec, available last price)
#we have concept data pos: all valid eps (non empty sec, available last price)
#we have new list pos:list of tickers maching valid data (non empty sec, available last price)
 
ratio_data_np = np.array(ratio_data_pos, dtype="float")
concept_data_np = np.array(concept_data_pos, dtype="float")



ordered_ratio_idx = np.argsort(ratio_data_np)

ordered_ratio = [ratio_data_pos[index] for index in ordered_ratio_idx]
ordered_ticker_list = [new_list_pos[index] for index in ordered_ratio_idx]
ordered_concept_data_np = [concept_data_pos[index] for index in ordered_ratio_idx]

order_length = len(ordered_concept_data_np)
reward = np.zeros(order_length)

print("ordered ratios: ")
print(ordered_ratio)
print("ordered concepts: ")
print(ordered_concept_data_np)
print("ordered corresponding ticker list:")
print(ordered_ticker_list)


for cntr,concept in enumerate(ordered_concept_data_np): 
    for cntr_2 in range(cntr+1,order_length): 
        if concept >= ordered_concept_data_np[cntr_2]: 
            reward[cntr] +=1

print("reward list is: ")
print(reward)

# plot_xy(reward)

results_idx = np.argsort(-reward)
print("results_idx is: ")
print(results_idx)
winner_tickers = [ordered_ticker_list[index] for index in results_idx]
print(winner_tickers)
