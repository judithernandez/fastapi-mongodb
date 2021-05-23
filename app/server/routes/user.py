import random
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_user,
    retrieve_user,
    login_user,
    save_auth_id,
    modify_user,
    retrieve_users_number,
)
from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()

# Create user - endpoint
@router.post("/", response_description="User data added into the database")
async def post_add_user_data(user: UserSchema = Body(...)):
	user = jsonable_encoder(user) 
	new_user = await add_user(user)
	return ResponseModel(new_user, "User added successfully.")

# Authenticate user - endpoint
@router.post("/login", response_description="User loged in")
async def post_user_login(email,password):
	try:
		#User exists?
		user_id = await login_user(email,password)
		#If login ok, give a unique auth_id to UserSchema
		auth_id = str(random.randint(100000,999999))
		await save_auth_id(user_id,auth_id)
		return ResponseModel({"auth_id": auth_id}, "User logged in successfully")
	except:
		return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")

# Private storage user data- endpoint (needs "auth_id")
@router.put("/{id}")
async def update_user_data(id: str, auth_id: int, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await modify_user(id, auth_id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} data update is successful".format(id),
            "User data updated successfully",
        )
    else:
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the user data.",
        )

# Private retrieve user data- endpoint (needs "auth_id")
@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id:str, auth_id: int):
    user = await retrieve_user(id, auth_id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")

# Public retrieve number of users in users_collection - endpoint
@router.get("/", response_description="Number of users retrieved")
async def get_users_number():
    cont = await retrieve_users_number()
    if cont:
        return ResponseModel({"Number of users": cont}, "Number of users retrieved successfully")
    return ResponseModel(users, "Empty list")



