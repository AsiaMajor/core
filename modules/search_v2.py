import pytest
import time
import csv
import redis
import hashlib

"""
redis-server
redis-cli

# seting hash format database
reader = csv.reader(csv_file,delimiter=',')
    for row in reader:
    r.hset("sheets", row[1], row[0])

"""
databaseName = "sheets"



r = redis.StrictRedis(host="localhost", port=6379, db=0)
#hget sheets sheetname -> returns "string format finger print"
#r.hgetall("sheets") # outputs all data 
# print(r.hget("sheets","sheet5_train_c.csv").decode('utf-8')) # returns fingerprints 
dataList=[]
for key in r.hkeys(databaseName):
    # print(key.decode('utf-8')) # shows each sheet name.
    dataList.append(key.decode('utf-8'))

# for i in dataList: # check if names of sheets are stored 
#     print(i)

input1 = "1100000111110111"  # temporary input


# def hamming_distance(chaine1, chaine2):
#     return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

# def hamming_distance2(chaine1, chaine2):
#     return len(list(filter(lambda x : ord(x[0])^ord(x[1]), zip(chaine1, chaine2))))


def hamming(a, b): # a == input fingerprint,  b == fingerprint from databasei
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

if __name__=="__main__":
    candidates = []
    distance = len(input1) 
    returnedDistance =0
    print(input1)
    for i in dataList:
        temFingerprint = r.hget(databaseName,i).decode('utf-8') # fingerprint
        returnedDistance = hamming(input1,temFingerprint)
        if returnedDistance <= distance:
            distance = returnedDistance # update pivot
            candidates.append(i+" "+temFingerprint+" "+str(distance) )
        #print(input1,temFingerprint,distance)

    print(len(candidates))  
    for i in candidates:
        print(i) # testing.
