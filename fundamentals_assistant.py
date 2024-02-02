import numpy as np 
import math
import yfinance as yf
import requests
from tqdm import tqdm
import pandas as pd 
import json
import matplotlib.pyplot as plt
import pprint
from datetime import datetime

# from extra import get_filtered_list
# sys.path.insert(8, '/home/yacbln/MyStuff/Programming/Github/database_assistant')
# from database_assistant import Database_Assistant
# sys.path.insert(9, '/home/yacbln/MyStuff/Programming/Github/graphing_assistant')
from graphing_assistant import Graphing_Assistant

from copy import deepcopy
from timing import tomorrow_date, today_date,last_business_day


class Fundamentals_Assistant: 
    from utils import get_ciks, get_company_fillings, get_company_facts, get_company_concept,test_only, get_trailing_eps
    from getting import get_specific_concept 
    def print_matrix_format(self,input_list):
        for i in range(0, len(input_list)):
            print(input_list[i])


    def __init__(self,reports,nbr_days,date_secretary,graphing_assistant): 
        self.enontiation = "=Fundamentals=Assistant=: "
        #Change these operational variables
        self.TESTING_ONLY = False
        self.PRINT_HISTOGRAM_ALL = False
        self.PRINT_HISTOGRAM_POSITIVES = False
        self.DO_POST_GRAPHING_ANALYSIS =False
        self.PRINT_REWARD_GRAPH = True 
        self.nbr_days = nbr_days

        self.reports = reports
        self.date_secretary = date_secretary
        self.graphing_guy = graphing_assistant

        self.ticker_cik_dict = self.get_ciks()


    def change_reports(self,new_reports): 
        self.reports = new_reports

        '''
    This method is very useful for backtesting
    '''
    def change_nbrdays(self,new_nbr_days): 
        self.nbr_days = new_nbr_days


    # def db_guy_ask_high(self): 

        
    #     db_guy= Database_Assistant()
    #     db_guy.read_data(batch_nbrs_used)

    def get_eps(self,types_list):
        ticker_cik_dict = self.get_ciks()
        # print("got here!")
        new_list, ratio_data, concept_data = [],[],[]
        new_list_pos, ratio_data_pos, concept_data_pos = [],[],[]
        nbr_invalids =0 
        nbr_neg_ratios = 0
        cntr =0

        invalids =[]
        nbr_invalid_concept_requests = 0
        nbr_invalid_concept_key = 0

    
        cik = ticker_cik_dict[self.ticker]
        print(cik)
        # exit(0)

        # company_fillings= get_company_fillings(cik)
        # simplified_fillings = company_fillings[['accessionNumber', 'reportDate', 'form']].head(50)

        # most_recent_filling  = simplified_fillings
        company_facts_usgaap = get_company_facts(cik)
        list_facts = company_facts_usgaap.keys()

        # print("all facts:", list_facts)
        # exit(0)
        #BA
        # TreasuryStockSharesAcquired
        # ShareBasedCompensation
        # TreasuryStockValueAcquiredCostMethod (cost mehod): shows effect on sell the purshased treasury 
        # (repurchase) in terms of increase/decrease of equity 
        # (Equity impact of the cost of common and preferred stock that were repurchased during the period. Recorded using the cost method.)
        # https://www.youtube.com/watch?v=MusfMph9xEQ
        # how does it change balance equation: reduction of assets (cash used to buy treasury stock) = reduction in equity
        # some/most can be going to employees -- how will they behave with stock -- maybe sell????

        listtt =[
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        # "Liabilities",
        # "StockholdersEquity",
        # "Assets",
        # "CommonStockSharesOutstanding",
        # "CommonStockSharesIssued",
        # "CommonStockSharesHeldInEmployeeTrustShares",
        # "CommonStockDividendsPerShareCashPaid",
        # "CommonStockDividendsPerShareDeclared",
        # "DividendsShareBasedCompensation",
        # "PreferredStockSharesIssued",
        # "ShareBasedCompensation",
        # "TreasuryStockCommonShares",
        # "TreasuryStockShares",
        # "StockRepurchasedDuringPeriodShares", #"Number of shares that have been repurchased during the period and have not been retired and are not held in treasury. Some state laws may govern the circumstances under which an entity may acquire its own stock and prescribe the accounting treatment therefore. This element is used when state law does not recognize treasury stock.
        # "TreasuryStockSharesAcquired",
        # "TreasuryStockValueAcquiredCostMethod",
        # "TreasuryStockAcquiredAverageCostPerShare",
        # "WeightedAverageNumberOfShareOutstandingBasicAndDiluted",
        # "WeightedAverageNumberOfSharesContingentlyIssuable",
        # "TreasuryStockCommonValue",
        ]

        # list =[
        # "Liabilities",
        # "StockholdersEquity",
        # "Assets",
        # "CommonStockSharesOutstanding",
        # "CommonStockSharesIssued",
        # "CommonStockSharesHeldInEmployeeTrustShares",
        # "CommonStockDividendsPerShareCashPaid",
        # "CommonStockDividendsPerShareDeclared",
        # "DividendsShareBasedCompensation",
        # "PreferredStockSharesIssued",
        # "ShareBasedCompensation",
        # "TreasuryStockCommonShares",
        # "TreasuryStockShares",
        # "TreasuryStockSharesAcquired",
        # "TreasuryStockValueAcquiredCostMethod",
        # "WeightedAverageNumberOfShareOutstandingBasicAndDiluted",
        # "WeightedAverageNumberOfSharesContingentlyIssuable",
        # "TreasuryStockCommonValue",
        # ]
        #liabilities not good, get it from asset

        dicts_to_graph = []
        for concept_name in listtt:
        # print(list_facts)
        # return list_facts
        # pp = pprint.PrettyPrinter()
        # pp.pprint(list_facts)
        #each fact (ex. Revenue, Assets) contains several entries as dictionary with filling date and form filed as some of the keys. 
            print("\n\n\n")
            print("=========================================")
            print(concept_name)
            print("=========================================")

            concept, response = get_company_concept(cik, concept_name)
            print(concept)
            # pd.set_option('display.max_columns', None)
            # pd.set_option('display.max_rows', None) 
            # print(concept)

            if response !=0:  
                if response == -1: 
                    nbr_invalid_concept_requests +=1
                    dicts_to_graph.append({})
                    continue
                elif response ==-2: 
                    nbr_invalid_concept_key +=1

            
            xy_dict = {"xvals":[], "yvals":[]}
            no_rep_dict = {}
            for dict in concept: 
                if dict['form'] == '10-K' or dict['form'] == '10-Q': 
                    if dict['end'] not in no_rep_dict.keys():
                        xy_dict["xvals"].append(dict['end'])
                        xy_dict["yvals"].append(dict['val'])
                        no_rep_dict[dict['end']] = 0
            
            dicts_to_graph.append(xy_dict)

        print("invalid concept requests :", nbr_invalid_concept_requests)
        # # filter the data
        # concept.form == '10-Q'
        # concept_10Q_only = concept
        #
        #[{'start': '2017-01-01', 'end': '2017-12-31', 'val': 124000000, 'accn': '0001543151-20-000010', 
        # 'fy': 2019, 'fp': 'FY', 'form': '10-K', 'filed': '2020-03-02', 'frame': 'CY2017'},
        # {'start': '2018-01-01', 'end': '2018-03-31', 'val': 61000000, 'accn': '0001628280-19-007524', 'fy': 2019, 
        # 'fp': 'Q1', 'form': '10-Q', 'filed': '2019-06-04', 'frame': 'CY2018Q1'}, 
        # {'start': '2018-01-01', 'end': '2018-06-30' ........

        graphing_guy = Graphing_Assistant()

        #prepare payloads
        datax,datay,title,xlabel,ylabel = [],[],[],[],[]
        for idx,dict in enumerate(dicts_to_graph): 
            try:
                xvals = dict["xvals"]
                yvals = dict["yvals"]
            except KeyError: 
                continue

            yvals_diff = np.diff(yvals)
            yvals_prc = yvals_diff / yvals[:-1] * 100
            yvals_prc = np.concatenate((np.array([0]),yvals_prc))
            yvals_prc_rd = np.round(yvals_prc, decimals=2)
            datax.append(xvals)
            datay.append(yvals_prc_rd)
            title.append(listtt[idx])
            xlabel.append("date")
            ylabel.append("prc chg")

        return {"datax":datax,"datay":datay,"title":title,"xlabel":xlabel,"ylabel":ylabel}

        # exit(0)
        # concept['form'] = concept['form'].astype(str)
        # concept_10Q_only = concept[concept.form.isin(['10-Q', '10-K', '10-Q/A', '10-K/A']) ]
        # # if ticker != "CVLT":
        # concept_10Q_only= concept_10Q_only.dropna(how='any')
        # concept_10Q_only = concept_10Q_only.reset_index(drop=True)
        
        # if concept_10Q_only.empty: 
        #     nbr_invalids+=1
        #     cntr+=1

        # results = tuple(None for _ in range(len(types_list)))

        # for idx,type in enumerate(types_list): 
        #     if type == "last": 
        #         res = concept_10Q_only.iloc[-1]['val']
        #     elif type == "trailing": 
        #         res = get_trailing_eps(concept)
        #     results[idx] = res
                
        # reversed_df = concept_10Q_only.iloc[::-1]

        # counter = 0
        # sett = set()
        # frame_skip=False
        # for index, row in reversed_df.iterrows():
        #     # print(row["frame"])
        #     if "frame" not in row: 
        #         print ("=======>ERROR: FRAME COLUMN DOES NOT EXIST!!!!")
        #         with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #             print(concept_10Q_only.to_string(index=False))
        #         frame_skip = True
        #         break

        #     if frame_skip: 
        #         frame_skip=False
        #         continue

        #     sett.add(row["frame"])
        #     counter +=1 


        # if len(sett) != 4: 
        #     print("----working on: ", ticker)
        #     print ("=======>ERROR: NON_CONTINGET!!!!")
        #     print(sett)

        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #             print(concept_10Q_only.to_string(index=False))
        
                
                
        #     exit(1)

        # years_cntr, quarter_cntr, invalid_cntr = 0,0,0
        # for frame in sett: 
        #     if len(frame) == 6: 
        #         years_cntr +=1
        #     elif len(frame) == 8: 
        #         quarter_cntr +=1
        #     else: 
        #         invalid_cntr +=1

        # # if years_cntr ==1 and quarter_cntr == (4-years_cntr) and invalid_cntr ==0: 
        # #     continue    
        
        # else:
        #     print("----working on: ", ticker)
        #     print ("=======>ERROR: NON_CONTINGET!!!!")
        #     print("years_cntr: ",years_cntr)
        #     print("quarter_cntr: ",quarter_cntr)
        #     print("invalid_cntr: ",invalid_cntr)
        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #         print(concept.to_string(index=False))
        
        # # continue

        # # if ticker == 'CVLT':
        # #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        # #         print(concept_10Q_only.to_string(index=False))


        # if trailing_yearly_eps is None:
        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #         print(concept_10Q_only.to_string(index=False))

        # # print("trailing eps: ", trailing_yearly_eps)
        
        # # print(concept_10Q_only)  
        # # exit(0)  
        # # if last_eps < 0: 
        # #     nbr_neg_ratios+=1
        # try:
        #     data_test = yf.download(ticker, start=last_business_day(), end=tomorrow_date(), progress=False)
        #     price = data_test[['Close']].iloc[0, 0]
        #     # print(price)
        # except: 
        #     nbr_invalids +=1
        #     cntr+=1
        #     progress_bar.update(1)
        #     # continue
        
        # concept_data.append(last_eps)
        # addition= 0 if last_eps==0 else price/last_eps
        # ratio_data.append(addition)
        # new_list.append(ticker)
        
        # if last_eps>0: 
        #     concept_data_pos.append(last_eps)
        #     ratio_data_pos.append(price/last_eps)
        #     new_list_pos.append(ticker)
        # cntr +=1
        # # print(concept_10Q_only)
        # # #try plotting
        # # concept_10Q_only.plot(x='end', y='val', kind='line')
        # # plt.title('Line Plot of DataFrame')
        # # plt.xlabel('x')
        # # plt.ylabel('y')
        # # plt.show()

        # #find histograms of price/eps valuation of companies belonging to a field or domain.
        # #put it alongsie the eps histogram and study the situation. 

        # #or instead of using your eyes to study the situation go over your thought process and replicate that in the form of 
        # #code, every thought process during the comparison or filtration is a step in the algorithm. Our brains solve problems, find optimal solutions 
        # #through a series of comparasion reward sytem
        # progress_bar.update(1)

        # progress_bar.close()

        # # print("ratios: ",ratio_data )
        # # print("number of negatives", nbr_neg_ratios)
        # print("\033[1m","number of valid companies (included in histogram): ",len_filtered_list- nbr_invalids,"\033[0m")
        # print("\033[1m","number of invalids (ex. no 10Q): ", nbr_invalids,"\033[0m")

        # #we have ratio data pos: all valid ratios (non empty sec, available last price)
        # #we have concept data pos: all valid eps (non empty sec, available last price)
        # #we have new list pos:list of tickers maching valid data (non empty sec, available last price)

        # ratio_data_all_np = np.array(ratio_data, dtype="float")
        # ratio_data_np = np.array(ratio_data_pos, dtype="float")
        # concept_data_np = np.array(concept_data_pos, dtype="float")

        # FLAGS = [PRINT_HISTOGRAM_ALL, PRINT_HISTOGRAM_POSITIVES]

        # plot_histogram(ratio_data_all_np, ratio_data_np, "P/E last quarter", FLAGS)


        # if not DO_POST_GRAPHING_ANALYSIS: 
        #     print("no post analysis requested")
        #     exit(0)

        # ordered_ratio_idx = np.argsort(ratio_data_np)
        # ordered_ratio = [ratio_data_np[index] for index in ordered_ratio_idx]
        # ordered_ticker_list = [new_list_pos[index] for index in ordered_ratio_idx]
        # ordered_concept_data = [concept_data_np[index] for index in ordered_ratio_idx]
        # order_length = len(ordered_concept_data)
        # reward = np.zeros(order_length)

        # #for testing
        # # print("ordered ratios: ")
        # # print(ordered_ratio)
        # # print("ordered_concepts: ")
        # # print(ordered_concept_data)
        # # print("ordered_corresponding ticker list:")
        # # print(ordered_ticker_list)


        # for cntr,concept in enumerate(ordered_concept_data): 
        #     for cntr_2 in range(cntr+1,order_length): 
        #         if concept >= ordered_concept_data[cntr_2]: 
        #             reward[cntr] +=1

        # # print("reward list is: ")
        # # print(reward)

        # if PRINT_REWARD_GRAPH:
        #     plot_xy(reward)

        # results_idx = np.argsort(-reward)
        # # print("results_idx is: ")
        # # print(results_idx)
        # winner_tickers = [ordered_ticker_list[index] for index in results_idx]
        # reward_winnners = np.array([reward[index] for index in results_idx])
        # ratio_winnners = np.array([ordered_ratio[index] for index in results_idx], dtype="float")
        # concept_winners= np.array([ordered_concept_data[index] for index in results_idx], dtype="float")

        # # print("ratio winners are: ", ratio_winnners)
        # # print("concept_winners are: ", -concept_winners)
        # ratio_indices = np.argsort(ratio_winnners)
        # # print("ratio indices: ", ratio_indices)
        # concept_indices = np.argsort(-1*concept_winners)
        # # print("concept indices: ", concept_indices)

        # ratio_ranks = np.zeros(order_length)
        # concept_ranks = np.zeros(order_length)

        # rank =1
        # for ratio_idx, concept_idx in zip(ratio_indices,concept_indices): 
        #     # print("adding to concept index: ", results_idx[concept_idx])
        #     # print("adding to ratio index: ", results_idx[ratio_idx])
        #     concept_ranks[concept_idx] = rank
        #     ratio_ranks[ratio_idx] = rank
        #     rank+=1

        # for rank,ticker in enumerate(winner_tickers): 
        #     print(f"{rank+1} - {ticker}: reward:{reward_winnners[rank]} ratio(rk. {ratio_ranks[rank]}): {ratio_winnners[rank]} eps(rk. {concept_ranks[rank]}): {concept_winners[rank]}")


# fund_object= Fundamentals_Assistant()
# res = fund_object.get_eps(["last"])
# fund_object.print_matrix_format(np.array([con for con in res]))

    def run_reports(self,payload):
        list_reports = self.reports
        if not list_reports:
            print(self.enontiation + "No reports have been assigned to me ..Yaaay!")
            return {payload["ticker"]:{}}
        
        self.ticker = payload["ticker"]
        try:
            self.first_day = payload["first_day"]
            self.data_open = payload["data_open"]
            self.data_close = payload["data_close"]
            self.data_high = payload["data_high"]
            self.data_low = payload["data_low"]
            self.data_vol= payload["data_volume"]
        except: 
            print(self.enontiation +"some data is not given - Pass since maybe intentional.")
            pass 

        # print(f"strategies assistant: attaching {self.ticker} with last price{self.data_high[-1]}")
        # exit(0)
        reports = {}
        if self.first_day == -1: 
            return {self.ticker:reports}
        results = None
        for report in list_reports: 
            print(f"running {report} for ticker {self.ticker}")

            # if report.startswith("getall:"):
            #     elements = report.split(':')[1]
            #     list_reports = elements.split(',')
                
            #     results = self.get_all(list_reports)
            
            #this section for new way of passing report list: name,paramet1,parameter2...as necessary
            if isinstance(report, list):
                if report[0] == "GetSpecificConcept":
                    results = self.get_specific_concept(report[1], graphing=True)


                reports[report[0]] = results

            #this section is for legacy way of doing things - passing report as string
            if isinstance(report, str):
                if report == "last_eps":
                    results = self.get_eps(["last"])
            
                
                reports[report] = results

        return {self.ticker:reports}