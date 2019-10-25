import pytest
#from modules.search import Search
from modules.preprocess import PreProcess
import pandas as pd
import numpy as np

def test_init_globals_avg():
    '''test global vaerages generated for fingerprinting'''
    sheet = [0,1,2,3,4,5,6,7,8,9]
    l,avg,std = PreProcess.get_wh_avg_std_data(sheet)
    
    assert l is list
    assert avg is list
    assert std is list

    assert l[0] is float
    assert avg[0] is float
    assert std[0] is float

    
def test_retrive_wheel_data(wheel_data):
    ''' test if the wheel data is correctly read in from db'''
    #assert wheel_data is 
    pass


# def test_retrive_column_data():
#     pass

def test_preprrocessing_new_sheet():
    ''' test if the input column is properly proprocessed'''
    pass