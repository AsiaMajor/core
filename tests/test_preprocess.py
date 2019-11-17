import pytest
from modules import preprocess
import pandas as pd
import numpy as np

# def test_PreProcess_init():
#     preprocess_agent = preprocess.Controller()
#     assert preprocess_agent is not None

def test_init_globals_avg():
    '''test global averages generated for fingerprinting'''
    # pass
    #path = "C:/git_repo/core/tests/sheet17_train_b.csv"
    path = "tests/test_sample/sheet17_train_b.csv"
    sheet = preprocess.Controller(path)
    l,avg,std = sheet.get_wh_avg_std_data(path)
    
    assert type(l) is list
    assert type(avg) is list
    assert type(std) is list

    assert type(l[0][0]) is str
    assert type(avg[0][0]) is str
    assert type(std[0][0]) is str

    
def test_retrive_wheel_data():
    ''' test if the wheel data is correctly read in from db'''
    # pass
    col_num = 0
    #path = "C:/git_repo/core/tests/sheet17_train_b.csv"
    path = "tests/test_sample/sheet17_train_b.csv"
    sheet = preprocess.Controller(path)
    df = [[1,2,3,4,5,6,7],[6,7,8,9,10,11,12]]
    out = sheet.get_n_column(df,col_num)

    assert type(out) is list
    assert type(out[0]) is float


# def test_retrive_column_data():
#     pass

def test_preprrocessing_new_sheet():
    ''' test if the thresh is properly preprocessed'''
    #pass
    #data = pd.DataFrame(range(1,101))
    path = "tests/test_sample/sheet17_train_b.csv"
    sheet = preprocess.Controller(path)
    data = np.random.randint(low=1, high=100, size=100)
    t3,t50,t97 = sheet.process_new_sheet(data)

    assert t3<t50
    assert t50<t97
    