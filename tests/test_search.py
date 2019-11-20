import pytest
from modules import search
# import redis

# f = open("tests/final.csv").readlines()

# data = []
# for line in f:
#       data.append(line.replace('\n', '').split(','))
# conn = redis.StrictRedis(host="localhost", port=6379, db=2)
# for sheet in data[1:]:
#      res = conn.hset(sheet[0], sheet[1], sheet[2])
#      if res == 0:
#              print(sheet, "NOT INSERTED")
#      else:
#              print(sheet, "OK")


"""
commnad : python3 -m pytest test_search.py 
"""
sheet1= "11111111111111111111"
sheet2= "11111111111111111100"

sheet3= "111111"
sheet4= "11111100"

sheet5 = "11111111111111111111"
sheet6 = "01010101010101010101"

sheet5_train_b_csv = "1001111000011000"
sheet6_train_b_csv = "1100111000011100"

# realTestData_Sheet6_train_b.csv = "1100111000011100"
# realClass = search.Controller(234,"input6","1100111000011100")



testClass = search.Controller(221,"sheet1","1111100000111110")
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

def test_database_connection_none_null():   # checks if the databse is conncected
    assert testClass.conn != None
    

# def test_result_none_null():    # checks if the get_result() returns result
#     testV = testClass.get_result()
#     assert testV != None


# def test_result_bucket_type():  # check the return type == dict
#     testV = testClass.get_result() 
#     assert type(testV) == dict


# def test_result_sheet_none_null(): # check if it returns matching sheet name
#     testV = testClass.get_result()
#     assert testV["predicted"] != None


# def test_result_candidates_none_null(): #check if it also gives candidates of matching sheets.
#     testV = testClass.get_result()
#     assert testV["top_five"] != []

# def test_name_of_result_with_real_data(): # test real data with database.
#     realV = realClass.get_result()
#     assert realV["predicted"] == "sheet6_train_b.csv" 

# def test_candidates_of_result_with_real_data():
#     realV = realClass.get_result()
#     assert len(realV["top_five"]) >= 1
