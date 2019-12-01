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


class Controller():

    def __init__(self, filepath):
        self.filepath = filepath

    def get_result(self):
        return self.gen_hash_keys_fing(self.filepath)

    def get_wh_avg_std_data(self, sheet):
        l = []
        avg = []
        std = []
        i = 0
        end = 0

        with open(sheet) as df:
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
    
        return l, avg, std

    def get_cavity_data(self, sheet):
        l = []

        with open(sheet) as df:
            r = csv.reader(df)
            start = 0
            for row in r:
                if 'Cavity 1' in row:
                    start = 1
                    
                if start == 1 and row != ["avg MC","stdev MC","avg SG","stdev Sg"]:
                    l.append(row)

                if row == ["avg MC","stdev MC","avg SG","stdev Sg"]:
                    break
                    
        return l[2:]

    def get_cavity(self, l, cav):
        data = []
        cavse = {'cav1': (1, 7), 'cav2': (8,14), 'cav3': (15,21), 'cav4': (22,28), 'cav5': (29,35), 'cav6': (36,42), 'cav7': (43,49)}

        start, end = cavse[cav]

        for row in l:
            data.append(row[start:end+1])

        return data


    #returns certain column from dataset
    def get_n_column(self, l, n):
        col = []

        for row in l:
            if len(row) == 7:
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
        yuka_v = str(euc_dist_sq)
        hash_key = yuka_v[:3]


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

       
        pvmfh, pvmsh, pufh, push, bev, mev, tev, intqv = 0,0,0,0,0,0,0,0
        beu, meu, teu, intqu, moe, sg, stdv, stdu = 0,0,0,0,0,0,0,0
        cav2, cav3, cav4, cav5, cav6 = 0,0,0,0,0
        
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

        #Features: 17-21
        
        cavity = self.get_cavity_data(sheet)

        '''
        CAVITIES 1 AND 7 ARE DOGSHIT
        '''
        c2 = self.get_cavity(cavity, 'cav2')
        c3 = self.get_cavity(cavity, 'cav3')
        c4 = self.get_cavity(cavity, 'cav4')
        c5 = self.get_cavity(cavity, 'cav5')
        c6 = self.get_cavity(cavity, 'cav6')
        
        cav2_df = self.get_n_column(c2, 4)
        cav3_df = self.get_n_column(c3, 4)
        cav4_df = self.get_n_column(c4, 4)
        cav5_df = self.get_n_column(c5, 4)
        cav6_df = self.get_n_column(c6, 4)
  
      
        if cav2_df[0] < -180000:
            cav2 = 1
        
        if cav3_df[0] < -175000:
            cav3 =1

        if cav4_df[0] < -87500:
            cav4 = 1
        
        if cav5_df[0] < -170000:
            cav5 = 1

        if cav6_df[0] < -82500:
            cav6 = 1
        

        temps = ''
        temps = temps + str(pvmfh) + str(pvmsh) + str(pufh) + str(push) + str(bev) + str(mev) + str(tev)
        temps = temps + str(intqv) + str(beu) + str(meu) + str(teu) + str(intqu) 
        temps = temps + str(moe) + str(sg) + str(stdv) + str(stdu)
        temps = temps + str(cav2) + str(cav3) + str(cav4) + str(cav5) + str(cav6)

        tempind = filename.find("/")
        tempfn = filename[tempind+1:]

        tempv = {}
        tempv['filename'] = tempfn
        tempv['hashkey'] = hash_key
        tempv['fingerprint'] = temps

        return tempv


