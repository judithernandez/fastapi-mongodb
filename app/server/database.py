import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

user_collection = database.get_collection("users_collection")


# Helpers for paring results from database query into Python dict
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "password": user["password"],
        "auth_id": user["auth_id"],
        "wallet": user["wallet"],
    }

# Add a new user into the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Authenticate a user with a matching email and password
async def login_user(email: str, password: str) -> dict:
    myquery = { "$and": [{ "email": email }, { "password": password }] }
    user = await user_collection.find_one(myquery)
    return user["_id"]

# Save auth_id to UserSchema
async def save_auth_id(id: str, auth_id: int) -> dict:
    query = {"_id": ObjectId(id)}
    new_values = {"$set" : {"auth_id": auth_id}}
    await user_collection.update_one(query,new_values)

# Update user data by searching for "_id"
async def modify_user(id: str, auth_id: int, data:dict):
    if len(data) < 1:
        return False
    myquery = { "_id": ObjectId(id) }
    user = await user_collection.find_one(myquery)
    if user:
        #If user is logged in
        if (user["auth_id"]==auth_id):
            updated_user = await user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            if updated_user:
                return True
            return False

# Select user data matching "_id" and "auth_id"
async def retrieve_user(id: str, auth_id: int) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        if (user["auth_id"]==auth_id):
            return user_helper(user)

# Select all users from user_collection
async def retrieve_users_number():
    cont = await user_collection.count_documents({})
    return cont