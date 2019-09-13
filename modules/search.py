import os
import pandas as pd
import csv
import numpy as np 
import math
from models import Sheet
from numpy import nan
from models import Sheet
from flask import jsonify
from decimal import Decimal
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class Search():

    def df_builder(self, feature_name):

        dict_of_features = {'avgmoe': Sheet.avgmoe, 'avgsg': Sheet.avgsg, 'avgmc': Sheet.avgsg, 'avgvel': Sheet.avgvel,
        'avgupt': Sheet.avgupt, 'pkdensity': Sheet.pkdensity, 'effvel': Sheet.effvel, 'lvel': Sheet.lvel, 'rvel': Sheet.rvel,
        'lupt': Sheet.lupt, 'rupt': Sheet.rupt, 'sg': Sheet.sg, 'mc': Sheet.mc}

        response = Sheet.query.with_entities(Sheet.sheet_label, dict_of_features[feature_name.lower()]).all()

        is_decimal = True
        try:
            float(response[0][1])
        except:
            is_decimal = False

        if is_decimal == True:
            master_label_data = [str(response[i][0]) for i in range(len(response))]
            master_number_data = [pd.Series(float(response[i][1])) for i in range(len(response))]
            df = pd.concat(master_number_data, axis=1, keys=[label for label in master_label_data])

        else:
            master_number_data = []
            master_label_data = []

            for i in range(len(response)):
                one_sheet_number_data = []
                #loop for list
                for data in response[i][1]:
                    if data != None:
                        one_sheet_number_data.append(float(data))
                    else:
                        one_sheet_number_data.append(nan)

                master_number_data.append(pd.Series(one_sheet_number_data))
                master_label_data.append(str(response[i][0]))
            df = pd.concat(master_number_data, axis=1, keys=[label for label in master_label_data])
        return df


    #return wheel feature_of_interest for input sheet 
    def wheel_feature_compiler(self, in_filename,feature_of_interest):
        columns = ["pos","EffVel","effUPT","LeftVel","LeftUPT","RightVel","RightUPT"]
        df = pd.DataFrame(columns=columns)
        input_file = open(in_filename)
        write_status = False

        for line in input_file:
            if line == '"Avg Vel","stdev Vel.","avg UPT","stdev UPT"\n':
                break
            if write_status:
                if(len(line.split(','))==len(df.columns)):
                    df.loc[len(df)]=[nan if (x=='""' or x == ''or x==None) else float(x) for x in line.replace('\n','').split(',')]
            if line == '"pos","EffVel","effUPT","LeftVel","LeftUPT","RightVel","RightUPT"\n':
                write_status = True
        
        return df[feature_of_interest]


    #return cavity feature_of_interest for input sheet 
    def cavity_feature_compiler(self, in_filename,feature_of_interest):
        columns = ["Row#","Position1","MC1","SG1","X1","dF1","ddB1","dQ1","Position2","MC2","SG2","X2","dF2","ddB2","dQ2","Position3","MC3","SG3","X3","dF3","ddB3","dQ3","Position4","MC4","SG4","X4","dF4","ddB4","dQ4","Position5","MC5","SG5","X5","dF5","ddB5","dQ5","Position6","MC6","SG6","X6","dF6","ddB6","dQ6","Position7","MC7","SG7","X7","dF7","ddB7","dQ7"]
        df = pd.DataFrame(columns =columns)
        input_file = open(in_filename)
        write_status = False

        for line in input_file:
            if line.split(',')[0] == '"avg MC"':
                break
            if write_status:
                if(len(line.split(','))==len(df.columns)):
                    df.loc[len(df)]=[nan if (x=='""' or x == '' or x==None) else float(x) for x in line.replace('\n','').split(',')]
            if line.split(',')[0] == '"Row#"':
                write_status = True
        
        return df[feature_of_interest]


    #produce complete_df with the input sheet as the last column
    def input_preprocess(self, in_filename,feature_of_interest):
        db_df = self.df_builder(feature_of_interest)

        if feature_of_interest == "EffVel":
            input_df = self.wheel_feature_compiler(in_filename,feature_of_interest)
            #input_df = input_df.dropna(thresh=int(0.95*(input_df.shape[0]))).reset_index()
            if input_df.shape[0]>len(db_df):
                input_df = input_df.drop(range(len(db_df),len(input_df)))
            complete_df = pd.concat((db_df,input_df),axis=1,sort=False)
            complete_df = complete_df.fillna(value = complete_df.mean(axis=0))
            complete_df = complete_df.sub(complete_df.mean(axis=0),axis=1)
            
        else:
            input_df = self.cavity_feature_compiler(in_filename,feature_of_interest)
            if input_df.shape[0]>len(db_df):
                input_df = input_df.drop(range(len(db_df),len(input_df)))
            complete_df = pd.concat((db_df,input_df),axis=1,sort=False)
            complete_df = complete_df.dropna(thresh=0.95*len(complete_df.columns)).reset_index(drop=True).drop(range(0,20)).reset_index(drop=True)
            complete_df = complete_df.fillna(value = complete_df.mean(axis=0))
            complete_df = complete_df.sub(complete_df.mean(axis=0),axis=1)
        
        return complete_df


    #use cos_similarity to compare
    def compare_input_with_db(self, complete_df,feature_of_interest,top_x):
        ratings={}
        result_dic={}
        for sheet in complete_df:
            print("sheet in complete_df loop running!")
            if sheet != feature_of_interest:
                print("sheet != feature_of_interest")
                rating = cosine_similarity(complete_df[feature_of_interest].values.reshape(1, -1),complete_df[sheet].values.reshape(1, -1))
                ratings[sheet] = {
                   "cosine_similarity_score": float(rating),
                #    # WE MIGHT WANNA QUERY LATER.
                   "avgMoe": float(Sheet.query.filter_by(sheet_label=sheet).first().avgmoe),
                   "avgSg": float(Sheet.query.filter_by(sheet_label=sheet).first().avgsg),
                   "avgMc": float(Sheet.query.filter_by(sheet_label=sheet).first().avgmc),
                   "avgVel": float(Sheet.query.filter_by(sheet_label=sheet).first().avgvel),
                   "avgUPT": float(Sheet.query.filter_by(sheet_label=sheet).first().avgupt),
                   "pkDensity": float(Sheet.query.filter_by(sheet_label=sheet).first().pkdensity) 
                }
                print("query performed.")
            print()
        sorted_ratings = sorted(ratings.items(), key=lambda item: item[1]['cosine_similarity_score'], reverse=True)
        result = sorted_ratings[0:top_x] #Array of lists

        #JSON building (if you want to add more metrics, add them here)
        for d in result:
            result_dic[d[0]] = d[1]
        
        return result_dic
   

    #reading in first chunk of data from csv (wheel data)
    def read_info_wheel(self, sheet):
        l = []
        i = 0

        #with open(os.path.join(cwd,path)) as df:
        with open(sheet) as df:
            r = csv.reader(df)
            for row in r:
                if i > 5 and row != ['Avg Vel', 'stdev Vel.', 'avg UPT', 'stdev UPT']:
                    l.append(row)
                if row == ['Avg Vel', 'stdev Vel.', 'avg UPT', 'stdev UPT']:
                    break
                i += 1
        #print(len(l))
        #print(l[-5:])
        return l

    def read_info_avg(self, sheet):
        l = []
        i = 0
        with open(sheet) as df:
            r = csv.reader(df)
            for row in r: 
                if i == 2:
                    #l.append(row)
                    #break
                    return row
                    
                i += 1
        return l 


    #returns certain column from dataset
    def get_n_column(self, l, n):
        col = []

        for row in l:
            if len(row) == 7:
                col.append(row[n])
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


    def get_vel_col(self, df, sheet):
        return df[sheet]

    #converting strings to float representation and replacing empty strings with 0
    def replacewithzero(self, l):
        #newl = [x if not isinstance(x,str) else 0 for x in l]
        newl = [float(x) if (x != '') else 0 for x in l]
        return newl

    def replaceNan(self, l):
        newl = [x if (math.isnan(x) == False) else 0 for x in l]
        return newl

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
            


    def filt(self, input, l):

        '''
        FEATURES:
        *vm = velocity slope 
        1) pos_vm_fhalf 3) pos_vm_shalf 5) avgmoe>2.0 6) avgsg > .545 
        7) avgmc > 4.95 8) avgvel > 5000  
        '''

        ipvmfh, ipvmsh, imoe, isg, imc, ivel, iupt, ithic, iden = 0, 0, 0, 0, 0, 0, 0, 0, 0

        #looking at input features
        in_wheel = self.read_info_wheel(input)
        in_wh_fh, in_wh_sh = self.get_halves(in_wheel)
        
        velcol = self.get_n_column(in_wh_fh, 1)
        newvelcol = self.replacewithzero(velcol)
        if self.see_trend(newvelcol) > 0:
            ipvmfh = 1
        
        velcol = self.get_n_column(in_wh_sh, 1)
        newvelcol = self.replacewithzero(velcol)
        if self.see_trend(newvelcol) > 0:
            ipvmsh = 1


        in_avg = self.read_info_avg(input)

        if float(in_avg[0]) > 2.0:
            imoe = 1
        if float(in_avg[1]) > .545:
            isg = 1
        if float(in_avg[2]) > 4.95:
            imc = 1
        if float(in_avg[3]) > 5000:
            ivel = 1
        if float(in_avg[4]) > 445:
            iupt = 1
        #if float(in_avg[7]) > .125:
            #ithic = 1
        if float(in_avg[10]) > .61:
            iden = 1
        
        input_name = 'input'

        #print(tokens[0],ipvmfh, ipvmsh, imoe, isg, imc, ivel, iupt, ithic, iden)

        the_list = []

        for i in l.keys():
            temp = []
            temp.append(i)

            wheel = self.df_builder('effVel')[i]
            #import pdb; pdb.set_trace()
            wh_fh = wheel[:int(len(wheel)/2)]
            wh_sh = wheel[int(len(wheel)/2):]

            newvelcol = self.replacewithzero(wh_fh)
            newvelcol = self.replaceNan(newvelcol)

            if self.see_trend(newvelcol) > 0:
                temp.append(1)
            else:
                temp.append(0)
            
            newvelcol = self.replacewithzero(wh_sh)
            newvelcol = self.replaceNan(newvelcol)
            if self.see_trend(newvelcol) > 0:
                temp.append(1)
            else:
                temp.append(0)

            #REST OF FEATURES
            if self.df_builder('avgmoe')[i][0] > 2.0:
                temp.append(1)
            else:
                temp.append(0)
            
            if self.df_builder('avgsg')[i][0] > .545:
                temp.append(1)
            else:
                temp.append(0)
            if self.df_builder('avgmc')[i][0] > 4.95:
                temp.append(1)
            else:
                temp.append(0)
            if self.df_builder('avgvel')[i][0] > 5000:
                temp.append(1)
            else:
                temp.append(0)
            if self.df_builder('avgupt')[i][0] > 445:
                temp.append(1)
            else:
                temp.append(0)
            '''
            if self.df_builder('avgthick')[i][0] > .545:
                temp.append(1)
            else:
                temp.append(0)
            '''
            temp.append(0)
            if self.df_builder('pkDensity')[i][0] > .545:
                temp.append(1)
            else:
                temp.append(0)

            the_list.append(temp)
        
        return([input_name,ipvmfh, ipvmsh, imoe, isg, imc, ivel, iupt, ithic, iden], the_list)


    def retrieveobt(self, inp, oup):
        for sheet in oup:
            i = 1
            obo = 0
            for b in inp[1:]:
                if b != sheet[i]:
                    obo += 1
                i+=1
            if obo < 3:
                return sheet

    def retrieveobo(self, inp, oup):
        for sheet in oup:
            i = 1
            obo = 0
            for b in inp[1:]:
                if b != sheet[i]:
                    obo += 1
                i+=1
            if obo < 2:
                return sheet
        return(self.retrieveobt(inp, oup))


    def identify(self, in_filename,feature_of_interest,top_x):
        complete_df = self.input_preprocess(in_filename,feature_of_interest)
        print("complete_df: ", complete_df)
        big_five = self.compare_input_with_db(complete_df,feature_of_interest,top_x)
        print("big_five: ", big_five)
        inp, oup = self.filt(in_filename, big_five)
        print("inp: ", inp)
        print("oup: ", oup)
        the_one = self.retrieveobo(inp, oup)
        print("the_one: ", the_one)

        return big_five, the_one[0]


    def analyze(input_file):
        print(input_file)
        search = Search()
        
        return search.identify(input_file,"EffVel",5)