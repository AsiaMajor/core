
import redis



#client = redis.Redis( host ='127.0.0.1', port=6379) # you can add password if you want
client = redis.Redis('localhost')



# client.set('language','Python')
# print(client.get('language'))


# client.set('language','Python', px = 10000)
# print(client.get('language'))
# print(client.ttl('language'))

client.mset({"Croatia": "Zagreb", "Bahamas":"Nassau"})
print(client.get("Croatia"))

# feature1 = {"sheet1": "1111", "sheet2": "2222", "sheet3":"3333"}
# feature2 = {"sheet1": "ABC", "sheet2": "BCA", "sheet3":"CAB"}
