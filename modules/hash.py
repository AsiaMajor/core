import os
import pandas as pd
import csv
import numpy as np 
import math
import time
from models import Sheet
from numpy import nan
from models import Sheet
from flask import jsonify
from decimal import Decimal
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

def hash_sheet(sheet_df,fingerprint):
  '''get the hash value for the sheet'''
  pass


#return wheel feature_of_interest for input sheet 
def wheel_feature_compiler(infile,feature_of_interest):
  columns = ["pos","EffVel","effUPT","LeftVel","LeftUPT","RightVel","RightUPT"]
  df = pd.DataFrame(columns=columns)
  write_status = False

  for line in infile:
    if line == '"Avg Vel","stdev Vel.","avg UPT","stdev UPT"\n':
      break
    if write_status:
      if(len(line.split(','))==len(df.columns)):
          df.loc[len(df)]=[nan if (x=='""' or x == ''or x==None) else float(x) for x in line.replace('\n','').split(',')]
    if line == '"pos","EffVel","effUPT","LeftVel","LeftUPT","RightVel","RightUPT"\n':
      write_status = True
  
  return df[feature_of_interest]

#produce complete_df with the input sheet as the last column
def input_preprocess(infile,feature_of_interest,baseline):
  print("1. Preprocessing input file...")

  if feature_of_interest == "EffVel":
    input_df = wheel_feature_compiler(infile,feature_of_interest)
    baseline = wheel_feature_compiler(baseline,feature_of_interest)
    #input_df = input_df.dropna(thresh=int(0.95*(input_df.shape[0]))).reset_index()
    if input_df.shape[0]>len(baseline):
      input_df = input_df.drop(range(len(baseline),len(input_df)))
    complete_df = pd.concat((baseline,input_df),axis=1,sort=False)
    complete_df = complete_df.fillna(value = complete_df.mean(axis=0))
    complete_df = complete_df.sub(complete_df.mean(axis=0),axis=1)
      
  # else:
  #   input_df = cavity_feature_compiler(infile,feature_of_interest)
  #   if input_df.shape[0]>len(baseline):
  #     input_df = input_df.drop(range(len(baseline),len(input_df)))
  #   complete_df = pd.concat((baseline,input_df),axis=1,sort=False)
  #   complete_df = complete_df.dropna(thresh=0.95*len(complete_df.columns)).reset_index(drop=True).drop(range(0,20)).reset_index(drop=True)
  #   complete_df = complete_df.fillna(value = complete_df.mean(axis=0))
  #   complete_df = complete_df.sub(complete_df.mean(axis=0),axis=1)
  return complete_df

#use cos_similarity to compare
def compare_input_with_db(complete_df,feature_of_interest):
  print("2. Comparing preprocessed file with DB...")
  ratings={}
  result_dic={}
  for sheet in complete_df:
      if sheet != feature_of_interest:
          rating = cosine_similarity(complete_df[feature_of_interest].values.reshape(1, -1),complete_df[sheet].values.reshape(1, -1))
          ratings[sheet] = {
              "cosine_similarity_score": float(rating),
          }
  sorted_ratings = sorted(ratings.items(), key=lambda item: item[1]['cosine_similarity_score'], reverse=True)
  #result = sorted_ratings[0:top_x] #Array of lists
  

  # #JSON building (if you want to add more metrics, add them here)
  # for d in result:
  #   query_result = Sheet.query.filter_by(sheet_label=d[0]).first()
  #   metrics = {
  #       "cosine_similarity_score": d[1]["cosine_similarity_score"],
  #       "avgMoe": float(query_result.avgmoe),
  #       "avgSg": float(query_result.avgsg),
  #       "avgMc": float(query_result.avgmc),
  #       "avgVel": float(query_result.avgvel),
  #       "avgUPT": float(query_result.avgupt),
  #       "pkDensity": float(query_result.pkdensity)
  #   }
  #   result_dic[d[0]] = metrics
  #return result_dic
  return sorted_ratings

if __name__ == "__main__":
  feature_of_interest = 'EffVel'
  baseline = open('D:/gdrive/cs423/datasets/sheet20/train/sheet20_train_a.csv')
  
  for sheet_number in range(1,139):
    for test_train in ['test','train']:
      for char_code in ['a','b','c','d']:
        in_filename = 'D:/gdrive/cs423/datasets/sheet' + str(sheet_number) + '/' + test_train + '/' + 'sheet' + str(sheet_number) + '_' + test_train + '_' + char_code + '.csv'
        infile = open(in_filename)

        complete_df = input_preprocess(infile,feature_of_interest,baseline)

