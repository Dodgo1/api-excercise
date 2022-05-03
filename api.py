from email.headerregistry import Address
import time
from typing import Optional
import pymongo
from fastapi import FastAPI
from pydantic import BaseModel

username = "username"
password = "password"
cluster_address = "cluster0"
# connection
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@{cluster_address}.fmeh0.mongodb.net/{cluster_address}?retryWrites=true&w=majority")
db = client["api_db"]
collection = db['db']

# API part
app = FastAPI()


class Item(BaseModel):
    index: int
    message: str


class UpdateItem(BaseModel):
    message: Optional[str] = None

@app.get("/")
async def root():
    # shows all of data
    all_data = list(collection.find({}))
    return all_data

@app.post("/create_item/")
def create_item(item: Item):
    # extra info about new message plus _id
    item_dict = item.__dict__
    # %c = Locale’s appropriate date and time representation.
    item_dict["time"] = time.strftime("%c", time.localtime())

    # change index to _id for mongo db, how to change auto index?, name _id causes problem with fast api i think?
    item_dict["_id"] = item_dict.pop("index")

    # auto "increment" mechanism
    while collection.find_one({"_id": item_dict["_id"]}):
        if collection.find_one({"_id": item_dict["_id"]}):
            item_dict["_id"] += 1
            continue
        else:
            return {f'Status":"Success - index has been changed to {item_dict["_id"]}'}

    collection.insert_one(item_dict)
    return {"Status": "Success"}


# delete
@app.delete("/delete/{index}")
def delete_item(index: int):
    collection.delete_one({"_id": index})
    return {"Status": "Success"}


# get by id
@app.get("/get_item/{index}")
def get_item(index: int):
    data = collection.find({"_id": index})
    dic = {}
    for n, i in enumerate(data):
        dic[n] = i
    if dic:
        return dic
    else: 
        return {"Status" : "0 results found"}


# get by message
@app.get("/get_item/{message}")
def get_item(message: str):
    data = collection.find({"message": message})
    dic = {}
    for n, i in enumerate(data):
        dic[n] = i
    if dic:
        return dic
    else: 
        return {"Status" : "0 results found"}


@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    match = collection.find_one({"_id": item_id})
    if not match:
        return {"Status": "No match"}

    if item.message is not None:
        # replace
        print(match)
        item = item.__dict__
        item["_id"] = match["_id"]
        item["time"] = time.strftime("%c", time.localtime())

        collection.replace_one({"_id": item_id}, item)
        return {"Status": "Done", "result": item}
