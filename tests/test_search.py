import pytest
from modules import search

 
 
"""
commnad : python3 -m pytest test_search.py 
"""
sheet1= "11111111111111111111"
sheet2= "11111111111111111100"

sheet3= "111111"
sheet4= "11111100"

sheet5 = "11111111111111111111"
sheet6 = "01010101010101010101"
testClass = search.Controller(1,"sheet1","1111100000111110")
                            # hashKey, sheetName, fingerPrint
                            # int,  string, string

def test_hamming_return_type():
    testV = testClass.hamming(sheet1,sheet2)
    assert type(testV) == int

def test_hamming_return_size(): # check if the return size is less than the length of shorter input
    testV = testClass.hamming(sheet3,sheet4) 
    tem = 0
    if len(sheet3)>len(sheet4):      # tem will store the size of fingerprint which is shorter than other one.
        tem = len(sheet4)
    else:
        tem = len(sheet3)
    assert testV <= tem

def test_hamming_return_value():        # test when 2 inputs have 10 different fingerprint values.
    testV = testClass.hamming(sheet5,sheet6) # expected output is 10.
    assert testV == 10

def test_database_connection_none_null():
    assert testClass.conn != None