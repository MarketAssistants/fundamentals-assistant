        
import copy
from datetime import datetime

def get_specific_concept(self, concept_list, graphing=False):

    cik = self.ticker_cik_dict[self.ticker]
    print(cik)
    # concept_name = "CommonStockSharesOutstanding"
    
    concepts_dict = {}
    for concept_name in concept_list:
        concept, response,unit = self.get_company_concept(cik, concept_name)
        # print(concept)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None) 
        print(f"---------- printing concept for ticker {self.ticker}: ",concept)

        if response == -1 or concept == -1: 
            print(self.enontiation + f" *********** Error getting concept: {concept_name}")
            continue


        xy_dict = {"xvals":[], "yvals":[]}
        no_rep_dict = {}
        for datis in concept.keys(): 

            print("looking for date: ", datis)
            # xy_dict["xvals"].append(self.date_secretary.get_date_index(datis, closest=True))
                
            xy_dict["xvals"].append(datetime.strptime(datis, "%Y-%m-%d"))    
            if concept_name == "Liabilities" or concept_name == 'StockholdersEquity' or concept_name == "Assets" or concept_name == "LiabilitiesCurrent":
                val = concept[datis]/200
            elif concept_name == "Revenues": 
                val = concept[datis]/50
            else: 
                val = concept[datis]
            # val = concept[datis]
            xy_dict["yvals"].append(val)

        # y_values = copy.deepcopy(xy_dict["yvals"])
        # xy_dict["yvals"][0] = 0
        # for i in range(1,len(y_values)): 
        #     print()
        #     xy_dict["yvals"][i] = round(100*(y_values[i]-y_values[i-1])/y_values[i-1],2)

        #convert to percent changes
        concepts_dict[concept_name] = xy_dict

        # if graphing: 
        #      self.graphing_guy.plot_xy_single(xy_dict["xvals"],xy_dict["yvals"],concept_name,"dates",unit)

    if graphing:
        print(f"got here.......to graph....ticker: {self.ticker}")
        xy_all = {"xvals":[], "yvals":[]}
        title_all = []
        xlabel_all = []
        ylabel_all = []
        for concept_key in concepts_dict.keys(): 
            xy_all["xvals"].append(concepts_dict[concept_key]["xvals"])
            xy_all["yvals"].append(concepts_dict[concept_key]["yvals"])
            title_all.append(concept_key)
            xlabel_all.append("dates")
            ylabel_all.append(concept_key)

        

        self.graphing_guy.plot_xy_same(xy_all["xvals"],xy_all["yvals"],title_all,xlabel_all,ylabel_all)

        ##this is the opportunity to add another graph and to show dates
        ##lets add volume and lets add low price along side dates showing according to  

        #1. first get the longest date series in graph
        # max_xidx = -1
        # min_xidx = 10000
        # for concept_key in concepts_dict.keys(): 
        #     xidx_first = concepts_dict[concept_key]["xvals"][0]
        #     xidx_last = concepts_dict[concept_key]["xvals"][-1]
        #     if xidx_first < min_xidx: 
        #         min_xidx = xidx_first
        #     if xidx_last > max_xidx: 
        #         max_xidx = xidx_last
        
        # data_x_1,data_x_2 = [],[]
        # data_y_1,data_y_2 = [],[]
        # for day in range(min_xidx,max_xidx+1): 
        #     date = self.date_secretary.get_date(day)
        #     data_x_1.append(date)
        #     data_x_2.append(date)

        #     data_y_1.append(self.data_close[day])
        #     sum_vol = 0
        #     for goback in range(0,10): 
        #         sum_vol += self.data_vol[day-goback]
        #     sum_vol = sum_vol/10
        #     data_y_2.append(sum_vol/(pow(10,6)/2))


        # data_x = [data_x_1,data_x_2]
        # data_y = [data_y_1,data_y_2]
        # x_label = ["dates","dates"]
        # y_label = ["close_price","10davgvolume"]
        # title = ["close_price","10davgvolume"]
        # self.graphing_guy.plot_xy_same(data_x,data_y,x_label,y_label,title)

    
    return concepts_dict