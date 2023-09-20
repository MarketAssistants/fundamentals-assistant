import numpy as np 
import requests
import pandas as pd 
import json
import matplotlib.pyplot as plt
import pprint


from utils import get_ciks, get_company_fillings, get_company_facts, get_company_concept

ticker_cik_dict = get_ciks()

cik = ticker_cik_dict['AAPL']
print(cik)

company_fillings= get_company_fillings(cik)
simplified_fillings = company_fillings[['accessionNumber', 'reportDate', 'form']].head(50)

most_recent_filling  = simplified_fillings.iloc[0]

company_facts_usgaap = get_company_facts(cik)
list_facts = company_facts_usgaap.keys()

pp = pprint.PrettyPrinter()
# pp.pprint(list_facts)

#each fact (ex. Revenue, Assets) contains several entries as dictionary with filling date and form filed as some of the keys. 
# concept = get_company_concept(cik, "EarningsPerShareDiluted")
# # print(concept)

# #check structure
# # print(concept.columns)
# # print(concept.form)

# # filter the data
# concept_10Q_only = concept[concept.form == '10-Q']
# #drops the original index (first column) makes new indexes incrementing due to filtered data only (no gaps)
# concept_10Q_only = concept_10Q_only.reset_index(drop=True)

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