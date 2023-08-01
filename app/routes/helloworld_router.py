from fastapi import APIRouter, HTTPException
import logging.config

router = APIRouter()

# logging.config.fileConfig('../logging.conf', disable_existing_loggers=False)
#
# # get root logger
# logger = logging.getLogger(__name__)


@router.get("/")
async def hello():
    print("---> Hello World")
    return {"message": "Hello World"}


@router.get("/hiya")
async def hiya():
    print("---> Well Hi!")
    return {"message": "Well Hi!"}


@router.get("/bye")
async def bye():
    print("---> Bye!")
    return {"message": "Bye!"}


@router.get("/{user}")
async def hello_user(user: str):
    print(f"---> Hello {user}")
    return {"message": f"Hello {user}"}
