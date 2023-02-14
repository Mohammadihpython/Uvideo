# from functools import wraps
# from typing import Any, Callable, Optional
# import httpx

# from fastapi import Response
from passlib.context import CryptContext

LOGIN_ENDPOINT = "http://127.0.0.1:8001/login/"


# def auth_required(func: Callable) -> Callable:
#     @wraps(func)
#     async def wrapper(*args: Any, **kwargs: Any):
#         try:
#             response = httpx.post(
#                 url=LOGIN_ENDPOINT,
#                 headers={
#                     "Authorization": kwargs["authorization"],
#                 }, )

#             response.raise_for_status()
#             return await func(*args, **kwargs)
#         except HTTPError as error:
#             return Response(
#                 status_code=error.request.url
#             )

#     return wrapper

