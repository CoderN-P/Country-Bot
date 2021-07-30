import motor.motor_asyncio
import pymongo
import dns, os

client1 = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGO'])

db1 = client1.db_name

my_collection = db1.collection_name





async def find_flag(id):
  data = await my_collection.find_one({"_id": str(id)})
  return data['data']['flag']

async def find_lb():
  data = my_collection.find({}).sort("data.prestige", -1)
  data = await data.to_list(10)
  return data

async def find_lb2():
  data = my_collection.find({}).sort("data.coins", -1)
  data = await data.to_list(10)
  return data

  

async def delete_task(user_id):
  await my_collection.delete_one({"_id": str(user_id)})



async def find_inventory(user_id):
    inventory = dict(await my_collection.find_one({"_id": str(user_id)}))

    if inventory == None:
      raise Exception
    else:
      return inventory['inventory']

    




async def writing(arg):
   await my_collection.insert_one({"_id": str(arg[0]), "data" : {"name": arg[1], "population": arg[2], "multiplier": arg[3], "job": arg[4], "work_ethic": arg[5], "prestige": arg[6], "requirement": arg[7], "wars_played": arg[8], "wars_won": arg[9], "wars_lost": arg[10], "times_worked": arg[11], "coins": arg[12]}, 'inventory': {}})


  
async def reading(user_id):
    data = dict(await my_collection.find_one({"_id": str(user_id)}))
    if data == None:
      raise Exception
    else:
      data = data['data']
      return [list(data.values())]



async def update_war(arg):
  await my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {"data.name": arg[1], "data.population": arg[2], "data.multiplier": arg[3], "data.job": arg[4], "data.work_ethic": arg[5], "data.wars_played": arg[8], "data.wars_won": arg[9], "data.wars_lost": arg[10]}
   }
)



async def update_prestige(arg):
  await my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': 
     {"data.name": arg[1], "data.population": arg[2], "data.multiplier": arg[3], "data.job": arg[4], "data.work_ethic": arg[5], "data.prestige": arg[6], "data.requirement": arg[7]}
   })




async def update(arg):
  await my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {"data.name": arg[1], "data.population": arg[2], "data.multiplier": arg[3], "data.job": arg[4], "data.work_ethic": arg[5], "data.times_worked": arg[6]}
   }
)


async def count():
  doccount = await my_collection.count_documents({})
  return doccount




async def update_coins(arg):
  await my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {'data.coins': arg[1]}
   }
)



async def update_inventory(arg):
  await my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {'inventory': arg[1]}
   }
)






async def search_name(name):
  data = await my_collection.find_one({'data.name': name})
  data = [list(data['data'].values())]
  return data



db2 = client1.bot_updates
my_collection2 = db2.update_info



    
async def create_update(channel):
  data = await my_collection2.find_one({"_id": int(channel)})
  if data is not None:
    pass
  else:
    raise Exception
  await my_collection2.insert_one({"_id": int(channel)})



def findall():
  data = my_collection2.find({})
  return data



async def delete_update(channel):
  data = await my_collection2.find_one({"_id": int(channel)})
  if data is not None:
    pass
  else:
    raise Exception
  await my_collection2.delete_one({"_id": int(channel)})





prefixes_db = client1.prefixes.main



async def create_prefix(id, prefix):
  await prefixes_db.insert_one({'_id': str(id), 'prefix': prefix})

async def get_prefix(id):
  prefix = await prefixes_db.find_one({'_id': str(id)})
  return prefix['prefix']

async def update_prefix(id, prefix):
  await prefixes_db.update_one({'_id': str(id)}, {'$set': {'prefix': prefix}})

async def delete_prefix(id):
  await prefixes_db.delete_one({'_id': str(id)})

client3 = pymongo.MongoClient(os.getenv('MONGO'))
prefixes_db2 = client3.prefixes.main
def create_prefix2(id, prefix):
  prefixes_db2.insert_one({'_id': str(id), 'prefix': prefix})


def get_prefix2(id):
  prefix = prefixes_db2.find_one({'_id': str(id)})
  return prefix['prefix']
