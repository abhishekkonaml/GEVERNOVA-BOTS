from pymongo import MongoClient

client=MongoClient("mongodb://igbots-mongo-svc.igbots-core.svc.cluster.local:27017")

print(client)