import pytest
import time
import csv
import redis
import hashlib
import numpy as np

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
    
    def levensthein(self, seq1, seq2):
        seq1 = list(map(int, [num for num in seq1]))
        seq2 = list(map(int, [num for num in seq2]))
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y
        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
        return int(matrix[size_x - 1, size_y - 1])
    
    def cosine_sim(self, seq1, seq2):
        seq1 = list(map(int, [num for num in seq1]))
        seq2 = list(map(int, [num for num in seq2]))
        cos_sim = np.dot(seq1, seq2)/(np.linalg.norm(seq1), np.linalg.norm(seq2))
        return cos_sim.any()

    def euclidean(self, seq1, seq2):
        seq1 = list(map(int, [num for num in seq1]))
        seq2 = list(map(int, [num for num in seq2]))
        return np.linalg.norm(np.array(seq1)-np.array(seq2))
    
    def jaccard_similarity(self, list1, list2):
        list1 = list(map(int, [num for num in list1]))
        list2 = list(map(int, [num for num in list2]))
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection) / union

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
                "hamming": 0,
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
            form["hamming"] = dist
            form["priority"] = priority
            form["fingerprint"] = fin
            topsheets.append(form)

        sortedsh = sorted(topsheets, key = lambda i: (i['hamming'], i['priority']))
        try:
            theSheet = sortedsh[0]['name']
        except:
            theSheet = theSheet
        return {
            "input_fingerprint": self.fingerprint,
            "predicted": theSheet,
            "top_five": sortedsh[:5],
            "top_three": sortedsh[:3],
            "sheets_in_bucket": sortedsh,
        }
       
