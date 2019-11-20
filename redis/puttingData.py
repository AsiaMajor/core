import redis

# on github
#f = open("redis/final.csv").readlines()


# on local
f = open("../scripts/final.csv").readlines()
data = []
for line in f:
      data.append(line.replace('\n', '').split(','))
conn = redis.StrictRedis(host="localhost", port=6379, db=2)
for sheet in data[1:]:
     res = conn.hset(sheet[0], sheet[1], sheet[2])
     if res == 0:
             print(sheet, "NOT INSERTED")
     else:
             print(sheet, "OK")


# you can check all contents in the buckets 
# by running command hgetall [hashValue]
