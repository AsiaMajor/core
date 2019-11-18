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
        self.conn = redis.StrictRedis(host="localhost", port=6379, db=2)

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
        mainbucket = self.conn.hgetall(self.hash_key)
        upbucket = {}
        downbucket = {}
        final_bucket = {}

        try:
            upbucket = self.conn.hgetall(str(int(self.hash_key)+1))
        except:
            upbucket = {}
        try:
            downbucket = self.conn.hgetall(str(int(self.hash_key)-1))
        except:
            downbucket = {}

        final_bucket = mainbucket.copy()
        final_bucket.update(upbucket)
        final_bucket.update(downbucket)

        first = 100
        topsheets = {}
        theSheet = (0,0,0)

        print('in: ', self.fingerprint, self.sheet_name)
        for key,val in final_bucket.items():
            fin = val.decode("utf-8")
            name = key.decode("utf-8")

            dist = self.hamming(self.fingerprint, fin)
    
            if dist < first:
                theSheet = (name, fin, dist)
                first = dist
            topsheets[name] = dist

        sortedsh = sorted(topsheets.items(), key=lambda kv: kv[1])

        return {
            "predicted": theSheet[0],
            "top_five": sortedsh
        }
       