from fastapi import Body, HTTPException, status, Response, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.config import settings
from app.schimas import User, UserLightIn, UserLightOut
from motor.motor_asyncio import AsyncIOMotorClient
from app.jwt_authentication import AuthHandler

MONGO_HOST = settings.MONGO_HOST
MONGO_PORT = settings.MONGO_PORT
MONGO_USERNAME = settings.MONGO_INITDB_USERNAME
MONGO_PASSWORD = settings.MONGO_INITDB_PASSWORD

router = APIRouter(prefix="/auth", tags=['authentication'])
auth_handler = AuthHandler()


@router.on_event("startup")
async def get_db():
    user_db = AsyncIOMotorClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}').users
    router.users = user_db


@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model=UserLightOut)
async def sign_up(user: User = Body(...), ):
    user = jsonable_encoder(user)
    users_db = router.users
    user_db = await users_db.users.find_one({'phone_number': user["phone_number"]})
    if user_db:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="user with this phone number is exist please login"
                            )
    user["password"] = auth_handler.get_password_hash(user["password"])

    new_student = await users_db.users.insert_one(user)
    created_user = await users_db.users.find_one({"_id": new_student.inserted_id})
    token = auth_handler.encode_token(user["phone_number"])
    return JSONResponse(content={"user":user, "token":token}, status_code=status.HTTP_201_CREATED)
    # return{"u":created_user}


@router.post('/login', status_code=status.HTTP_200_OK, response_model=UserLightOut)
async def login(user: UserLightIn):
    user = jsonable_encoder(user)
    users_db = router.users
    user_db = await users_db.users.find_one({'phone_number': user["phone_number"]})
    
    if user_db:
        if auth_handler.verify_password(plain_text=user["password"], hashed_password=user_db["password"]):
            token = auth_handler.encode_token(user['phone_number'])
            return Response(status_code=status.HTTP_200_OK,content=token)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="wrong password")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
