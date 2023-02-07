import redis
import time
import json
from redis.commands.json.path import Path
from dotenv import load_dotenv
import os


load_dotenv()

client = redis.Redis(host=os.getenv('Redis_host'), port=os.getenv('Redis_port'),password=os.getenv('Redis_password'))

jane = {
     'name': "Jane",
     'Age': 33,
     'Location': "Chawton"
   }
brown = {
     'name': "brown",
     'Age': 33,
     'Location': "Chawton"
   }
test={"jan":jane,"brown":brown}
test={"jan":brown,"brown":brown}
client.json().set('person:1', Path.root_path(), test)
result = client.json().get('person:1')
print(result)

print(client.json().get('person:1'))