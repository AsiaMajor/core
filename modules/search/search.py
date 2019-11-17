import pytest
import time
import csv
import redis
import hashlib




class Controller():

    def __init__ (self, hash_key, sheet_name, fingerprint):
        self.hash_key = hash_key
        self.fingerprint = fingerprint
        self.sheet_name = sheet_name
        self.conn = redis.StrictRedis(host="localhost", port=6379, db=0)

    def hamming(self, a, b): # a == input fingerprint,  b == fingerprint from databasei
        # print(len(a),len(b))
        distance = 0
        front = 0
        back = 0
        if len(a)>len(b):
            back = len(b)-1
        else:
            back = len(a)-1
        while(front<back):
            if( a[front] != b[front]): # compare same index feature from front
                distance += 1 ## far
            if( a[back] != b[back]):   # same, but from back
                distance += 1 ## far
            front += 1
            back -= 1
        return distance

    def get_result(self):


        buckets = self.conn.hgetall(self.hash_key)
        return "yuka"



        # candidates = []
        # distance = len(input1) 
        # returnedDistance =0
        # print(input1)
        # for i in dataList:
        #     temFingerprint = r.hget(databaseName,i).decode('utf-8') # fingerprint
        #     returnedDistance = hamming(input1,temFingerprint)
        #     if returnedDistance <= distance:
        #         distance = returnedDistance # update pivot
        #         candidates.append(i+" "+temFingerprint+" "+str(distance) )
        #     #print(input1,temFingerprint,distance)

        # print(len(candidates))  
        # for i in candidates:
        #     print(i) # testing.


# f = open('final_csv').readlines()
# data = []
# for line in f:
#     data.append(line.replace('\n', '').split(','))

# for sheet_data in data:
#     conn.hset(sheet_data[0], sheet_data[2], sheet_data[1])