import os
import pandas as pd
import csv
import numpy as np 
import math
import time
import statistics 
from numpy import nan
from flask import jsonify
from decimal import Decimal
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


class PreProcess():

    def get_wh_avg_std_data(self, sheet):
        l = []
        avg = []
        std = []
        i = 0
        end = 0

        cwd = os.getcwd()
        path = 'dbfiles/' + sheet

        with open(os.path.join(cwd, path)) as df:
            r = csv.reader(df)
            for row in r:
                if i == 2:
                    avg.append(row)
                if i > 5 and row != ['Avg Vel', 'stdev Vel.', 'avg UPT', 'stdev UPT']:
                    l.append(row)
                if end == 1:
                    std.append(row)
                    break
                if row == ['Avg Vel', 'stdev Vel.', 'avg UPT', 'stdev UPT']:
                    end = 1
                i += 1
            
        #print(len(l))
        #print(l[-5:])
        return l, avg, std


    #returns certain column from dataset
    def get_n_column(self, l, n):
        col = []

        for row in l:
            if len(row) == 7:
                #col.append(row[n])
                try:
                    t = float(row[n])
                    col.append(t)
                except ValueError:
                    t = row[n]
        return col


    def get_halves(self, l):

        i = 0
        fhalf, shalf = [], []

        for row in l:
            if (i < len(l)/2):
                fhalf.append(row)
            else:
                shalf.append(row)
            i += 1
        return fhalf, shalf

    def trendline(self, data, order=1):
        coeffs = np.polyfit(data.index.values, list(data), order)
        slope = coeffs[-2]
        return float(slope)

    def see_trend(self, l):

        x = [i for i in range(0,len(l))]
        df = pd.DataFrame({'x':x, 'y':l})
        slope = self.trendline(df['y'])
        #print(slope)
        return slope


    def parse(self, s, deli):
        l = []
        temps = ''

        for ch in s:
            if ch != deli and ch != s[-1]:
                temps += ch
            elif ch != deli and ch == s[-1]:
                temps += s[-1]
                l.append(temps)
            else:
                l.append(temps)
                temps = ''
        return(l)


    avg_3percent_thresh = 400
    def process_new_sheet(self, data):
        '''take in new sheet, calculate the 3% 50% 97% thresh'''
        data =sorted(data)
        thresh_3 = max(data[0:int(len(data)*0.03)])
        thresh_50 = statistics.median(data)
        thresh_97 = min(data[int(len(data)*0.97):len(data)])

        #range_3_50 = thresh_50 - thresh_3
        #range_50_97 = thresh_97 - thresh_50
        #kurtosis = np.mean(scipy.stats.kurtosis(data))

        return thresh_3,thresh_50,thresh_97





    #takes in csv file 'sheet'
    #generates value that we will hash on
    #also generates fingerprint
    def gen_hash_keys_fing(self, sheet):

        filename = os.fsdecode(sheet)
        wh_info, avgs, std = self.get_wh_avg_std_data(sheet)
        effv_col = self.get_n_column(wh_info, 1)

        '''
        ********************************************************************
        1) GENERATING VALUE TO HASH ON - SQUARED EUCLIDEAN
        ********************************************************************
        '''
        # - base line will be straigh line, could've used an actuals sheets
        #   effv col but then we would have to verify lengths
        base = [1.0]
        base = base * len(effv_col)

        #converting to np arrays
        a = np.array(effv_col)
        b = np.array(base)

        #euclidean distance
        euc_dist = np.linalg.norm(a-b)

        #squared euc dist 
        euc_dist_sq = euc_dist * euc_dist

        #VALUE USED AS HASH KEY
        hash_key = euc_dist_sq[:3]


        '''
        ******************************************************************************************************
        2) GENERATING FINGERPRINT
        ******************************************************************************************************
        '''
        averages_v = {'bot3': 4649.704278448665, 'mid': 5140.350671570251, 'top3': 5485.360766006317, 'intq': 835.6564875576523, 'std': 243.80527702771303}
        averages_u = {'bot3': 405.8229635175804, 'mid': 434.35474998381557, 'top3': 480.89370725254514, 'intq': 75.07074373496476, 'std': 21.761536830164825}

        '''
        1) pos_vm_fhalf 2) pos_vm_shalf 3) pos_up_fhalf, 4) pos_up_shalf 5) bot_eff_vel 6) mid_eff_vel
        7) top_eff_vel 8) intq_eff_vel 9) bot_eff_upt 10) mid_eff_upt 11) top_eff_upt 12) intq_eff_upt 
        13) avgmoe 14) avgsg 15) std_dev_vel 16) std_dev_upt 
        '''

        #mightve made mistake in create_fingprint with intqeu

        pvmfh, pvmsh, pufh, push, bev, mev, tev, intqv = 0,0,0,0,0,0,0,0
        beu, meu, teu, intqu, moe, sg, stdv, stdu = 0,0,0,0,0,0,0,0

        
        wh_fh, wh_sh = self.get_halves(wh_info)

        #Features: 1-2
        vel_col_fh = self.get_n_column(wh_fh, 1)
        vel_col_sh = self.get_n_column(wh_sh, 1)

        if self.see_trend(vel_col_fh) > 0:
            pvmfh = 1
        if self.see_trend(vel_col_sh) > 0:
            pvmsh = 1 

        #Features: 3-4
        upt_col_fh = self.get_n_column(wh_fh, 2)
        upt_col_sh = self.get_n_column(wh_sh, 2)

        if self.see_trend(upt_col_fh) > 0:
            pufh = 1
        if self.see_trend(upt_col_sh) > 0:
            push = 1
        
        #Features: 5-8
        col_infor_v = self.get_n_column(wh_info, 1)
        bot3v, av, top3v = self.process_new_sheet(col_infor_v)

        if bot3v > averages_v["bot3"]:
            bev = 1
        if av > averages_v["mid"]:
            mev = 1
        if top3v > averages_v["top3"]:
            tev = 1
        if averages_v['intq'] < (top3v-bot3v):
            intqv = 1

        #Features: 9-12
        col_infor_u = self.get_n_column(wh_info, 2) #2 is effupt
        bot3u, au, top3u = self.process_new_sheet(col_infor_u)

        if bot3u > averages_u["bot3"]:
            beu = 1
        if au > averages_u['mid']:
            meu = 1
        if top3u > averages_u['top3']:
            teu = 1
        if averages_u['intq'] < (top3u-bot3u):
            intqu = 1

        #Features: 13-14
        if float(avgs[0][0]) > 2.0:
            moe = 1
        if float(avgs[0][1]) > .545:
            sg = 1

        #Features: 15-16
        if float(std[0][1]) > averages_v['std']:
            stdv = 1
        if float(std[0][3]) > averages_u['std']:
            stdu = 1
        

        fing = [filename, [pvmfh, pvmsh, pufh, push, bev, mev, tev, intqv, beu, meu, teu, intqu, moe, sg, stdv, stdu]]

        return hash_key, fing


