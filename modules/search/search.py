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
        up2bucket = {}
        up3bucket = {}
        down3bucket = {}
        down2bucket = {}
        downbucket = {}
        final_bucket = {}

        try:
            upbucket = self.conn.hgetall(str(int(self.hash_key)+1))
            up2bucket = self.conn.hgetall(str(int(self.hash_key)+2))
            up3bucket = self.conn.hgetall(str(int(self.hash_key)+3))
            downbucket = self.conn.hgetall(str(int(self.hash_key)-1))
            down2bucket = self.conn.hgetall(str(int(self.hash_key)-2))
            down3bucket = self.conn.hgetall(str(int(self.hash_key)-3))
        except:
            pass

        final_bucket = mainbucket.copy()
        final_bucket.update(upbucket)
        final_bucket.update(up2bucket)
        final_bucket.update(up3bucket)
        final_bucket.update(downbucket)
        final_bucket.update(down2bucket)
        final_bucket.update(down3bucket)

        first = 100
        topsheets = []
        theSheet = (0,0,0)

        for key,val in final_bucket.items():
            fin = val.decode("utf-8")
            name = key.decode("utf-8")
            form = {
                "name": "",
                "hamming_distance": 0,
                "priority": 0,
                "fingerprint": ""
            }

            dist = self.hamming(self.fingerprint, fin)
    
            if dist < first:
                theSheet = (name, fin, dist)
                first = dist

            if key in mainbucket.keys():
                priority = 1
            if key in upbucket.keys() or key in downbucket.keys():
                priority = 2
            if key in up2bucket.keys() or key in down2bucket.keys():
                priority = 3
            if key in up3bucket.keys() or key in down3bucket.keys():
                priority = 4

            form["name"] = name
            form["hamming_distance"] = dist
            form["priority"] = priority
            form["fingerprint"] = fin
            topsheets.append(form)


        sortedsh = sorted(topsheets, key = lambda i: (i['priority'], i['hamming_distance']))

        return {
            "predicted": theSheet[0],
            "top_five": sortedsh
        }
       
