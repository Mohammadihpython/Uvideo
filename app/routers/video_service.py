import binascii
import os

from fastapi import APIRouter, BackgroundTasks, UploadFile, Request, Form, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from ..config import settings
from ..jwt_authentication import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()


@router.on_event("startup")
async def get_mongodb():
    video_db = AsyncIOMotorClient(
        f'mongodb://{settings.MONGO_INITDB_USERNAME}:{settings.MONGO_INITDB_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}').video
    router.library = video_db.library
    router.fs = AsyncIOMotorGridFSBucket(video_db)


async def _generate_hash():
    return binascii.hexlify(os.urandom(16)).decode('utf-8')

async def _get_videos(user=Depends(auth_handler.auth_wraper)):
    videos = router.library.find({'phone_number': user})
    docs = await videos.to_list(None)
    video_urls = ''
    for i in docs:
        filename = i['filename']
        v = f'<a href="{settings.PROTOCOL}://{settings.MONGO_HOST}/stream/{filename}" target="_blank">http://{HOST}/stream/{filename}</a>'
        video_urls = video_urls + '<br>' + v
    return video_urls


@router.get('/')
async def index(user=Depends(auth_handler.auth_wraper)):
    videos = await _get_videos(user)
    return HTMLResponse(videos)


async def _add_library_record(hash: str, user=Depends(auth_handler.auth_wraper), ):
    data = { 'filename': hash,'user_phone_number': user,}
    await router.library.insert_one(data)


async def _upload(file: object, hash: str):
    grid_in = router.fs.open_upload_stream(
        hash, metadata={'contentType': 'video/mp4'})
    data = await file.read()
    await grid_in.write(data)
    await grid_in.close()  # uploaded on close

@router.post('/upload')
async def upload(file: UploadFile, background_tasks: BackgroundTasks,user=Depends(auth_handler.auth_wraper)):
    if user:
        if file.filename:
            hash = await _generate_hash()
            background_tasks.add_task(_upload, file, hash)
            background_tasks.add_task(_add_library_record, user, hash)
            videos = await _get_videos(user)
            return {videos: videos}


@router.get('/stream/{filename}')
async def stream(filename: str, user=Depends(auth_handler.auth_wraper)):
    if user:
        grid_out = await router.fs.open_download_stream_by_name(filename)

        async def read():
            while grid_out.tell() < grid_out.length:
                yield await grid_out.readchunk()

        return StreamingResponse(read(), media_type='video/mp4',
                                 headers={'Content-Length': str(grid_out.length)})
