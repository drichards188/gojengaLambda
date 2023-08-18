from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi import Request, Header
import logging.config

from starlette import status

from app.common.Auth import get_current_active_user
from app.common.Lib import Lib
from app.handlers.account_handler import AccountHandler
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.User import User

router = APIRouter()

logger = logging.getLogger(__name__)


# logging.config.fileConfig('../logging.conf', disable_existing_loggers=False)
#
# # get root logger
# logger = logging.getLogger(__name__)

@router.get("/{username}", tags=["Account"])
async def get_user(request: Request, username: str, is_test: Optional[bool] | None = Header(default=False),
                   current_user: User = Depends(get_current_active_user)):
    if Lib.detect_special_characters(username):
        raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
    try:
        print(f'--> trying to get account {username}')
        account = AccountHandler.handle_get_account(username.lower(), is_test)
        return {"response": account}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", tags=["Account"])
async def post_account(request: Request, data: Account, is_test: Optional[bool] | None = Header(default=False),
                       current_user: User = Depends(get_current_active_user)):
    try:
        if Lib.detect_special_characters(data.name):
            raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')

        resp = AccountHandler.handle_create_account(data.name, data.balance, is_test)
        return {"response": resp}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{username}", tags=["Account"])
async def put_user(request: Request, username: str, data: Account,
                   is_test: Optional[bool] | None = Header(default=False),
                   current_user: User = Depends(get_current_active_user)):
    if Lib.detect_special_characters(username):
        raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
    try:
        resp = AccountHandler.handle_update_account(username.lower(), data.balance, is_test)
        return {"response": resp}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{username}", tags=["Account"])
async def delete_user(request: Request, username: str, is_test: Optional[bool] | None = Header(default=False),
                      current_user: User = Depends(get_current_active_user)):
    if Lib.detect_special_characters(username):
        raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
    try:
        resp = AccountHandler.handle_delete_account(username.lower(), is_test)
        return {"response": resp}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{username}/deposit", tags=["Deposit"])
async def post_deposit(request: Request, username: str, data: Account,
                       is_test: Optional[bool] | None = Header(default=False),
                       current_user: User = Depends(get_current_active_user)):
        try:
            if Lib.detect_special_characters(username):
                raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
            print(username)
            resp = AccountHandler.handle_modify_account(username.lower(), data.balance, is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{username}/transaction", tags=["Transaction"])
async def post_transaction(request: Request, username: str, data: Transaction,
                           is_test: Optional[bool] | None = Header(default=False),
                           current_user: User = Depends(get_current_active_user)):
        try:
            if Lib.detect_special_characters(data.sender) or Lib.detect_special_characters(data.receiver):
                raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT,
                                    detail='please send legal sender and receiver')

            resp = AccountHandler.handle_transaction(data.sender, data.receiver, data.amount, is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
