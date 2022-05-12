import time
import secrets
import os
from typing import Optional
import pymongo
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

description = """
Przykładowe api, korzystające z mongodb

***Dane potrzebne do połączenia się należy uzupełnić w pliku <i>.env</i>***
"""


tags_metadata = [
    {
        "name":"root",
        "description":"Shows all data after authentication"
    },
    {
        "name":"users",
        "description" : "user management"
    },
    {
        "name":"items",
        "description":"items management"
    }

]

load_dotenv()

username = os.getenv("USERNAME_MONGODB")
password = os.getenv("PASSWORD")
cluster_address = os.getenv("CLUSTER_ADDRESS")

# connection
client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@{cluster_address}.fmeh0.mongodb.net/{cluster_address}?retryWrites=true&w=majority")
db = client["api_db"]
collection = db['db']
collection_users = db["db_users"]

# API part
app = FastAPI(
    openapi_tags=tags_metadata,
    description=description,
    title="api-excercise",
    version="1.0.1",
    contact={
        "name":"Adam Jaskierski",
        "email": "a.jaskierski@tkhtechnology.com"
    }
    )

security = HTTPBasic()


class Item(BaseModel):
    index: int
    message: str


class UpdateItem(BaseModel):
    message: Optional[str] = None


class User(BaseModel):
    username: str
    password: str


# test using curl -u username:passwd /// browser remembers credentials
# has pass and store in db
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    # read users from db_users
    correct_username = secrets.compare_digest(credentials.username, "test1")
    correct_password = secrets.compare_digest(credentials.password, "pass1")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", tags=["root"])
async def root(current_user: str = Depends(get_current_username)):
    # shows all of data
    all_data = list(collection.find({}))
    return all_data


@app.get("/gets/user",tags=["users"])
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.post("/posts/users",tags=["users"])
def create_user(user: User):
    #insert users
    collection_users.insert_one(user.__dict__)
    return {"Status": "Success"}


@app.post("/posts/item",tags=["items"])
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
@app.delete("/deletes/itemIndex/{index}",tags=["items"])
def delete_item(index: int):
    collection.delete_one({"_id": index})
    return {"Status": "Success"}


# get by id
@app.get("/gets/itemIndex/{index}",tags=["items"])
def get_item(index: int):
    data = collection.find({"_id": index})
    dic = {}
    for n, i in enumerate(data):
        dic[n] = i
    if dic:
        return dic
    else:
        return {"Status": "0 results found"}


# get by message
@app.get("/gets/itemMessage/{message}",tags=["items"])
def get_item(message: str):
    data = collection.find({"message": message})
    dic = {}
    for n, i in enumerate(data):
        dic[n] = i
    if dic:
        return dic
    else:
        return {"Status": "0 results found"}


@app.put("/puts/itemId/{item_id}",tags=["items"])
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
