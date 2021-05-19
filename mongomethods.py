import pymongo
import dns, os

client1 = pymongo.MongoClient(os.environ['MONGO'])

db1 = client1.db_name

my_collection = db1.collection_name

def user_exists(user_id):
  check = list(my_collection.find({"_id": str(user_id)}))
  if len(check) == 0:
    return False
  else:
    return True

def delete_task(user_id):
  my_collection.delete_one({"_id": str(user_id)})

def find_inventory(user_id):
  if user_exists(user_id) == False:
     raise Exception('User does not have country')
     return

  return my_collection.find_one({"_id": str(user_id)})['inventory']


def writing(arg):
   my_collection.insert_one({"_id": str(arg[0]), "data" : {"name": arg[1], "population": arg[2], "multiplier": arg[3], "job": arg[4], "work_ethic": arg[5], "prestige": arg[6], "requirement": arg[7], "wars_played": arg[8], "wars_won": arg[9], "wars_lost": arg[10], "times_worked": arg[11], "coins": arg[12]}, 'inventory': {}})

def reading(user_id):
   if user_exists(user_id) == False:
     raise Exception('User does not have country')
     return
   return [list(my_collection.find_one({"_id": str(user_id)})['data'].values())]

def update_war(arg):
  a = reading(arg[0])
  my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {"data.name": arg[1], "data.population": arg[2], "data.multiplier": arg[3], "data.job": arg[4], "data.work_ethic": arg[5], "data.wars_played": arg[8], "data.wars_won": arg[9], "data.wars_lost": arg[10]}
   }
)
def update_prestige(arg):
  a = reading(arg[0])
  my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': 
     {"data.name": arg[1], "data.population": arg[2], "data.multiplier": arg[3], "data.job": arg[4], "data.work_ethic": arg[5], "data.prestige": arg[6], "data.requirement": arg[7]}
   })

def update(arg):
  a = reading(arg[0])
  my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {"data.name": arg[1], "data.population": arg[2], "data.multiplier": arg[3], "data.job": arg[4], "data.work_ethic": arg[5], "data.times_worked": arg[6]}
   }
)

def count():
  return my_collection.count()


def update_coins(arg):
  a = reading(arg[0])
  my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {'data.coins': arg[1]}
   }
)



def update_inventory(arg):
  a = reading(arg[0])
  my_collection.update_one(
   {"_id": str(arg[0])},
   {
     '$set': {'inventory': arg[1]}
   }
)




def search_name(name):
  data = [list(my_collection.find_one({'data.name': name})['data'].values())]
  return data

db2 = client1.bot_updates
my_collection2 = db2.update_info
def check_channel(channel):
  if my_collection2.find_one({"_id": int(channel)}) is not None:
    return False
  else:
    return True
    
def create_update(channel):
  if check_channel(channel) == False:
    raise Exception
  else:
    pass
  my_collection2.insert_one({"_id": int(channel)})

def findall():
  return my_collection2.find()

def delete_update(channel):
  if check_channel(channel) == True:
    raise Exception
  else:
    pass
  my_collection2.delete_one({"_id": int(channel)})


