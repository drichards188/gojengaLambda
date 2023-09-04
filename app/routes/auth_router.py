import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Request, Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.common import Auth
from app.common.Auth import Token, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    REFRESH_ACCESS_TOKEN_EXPIRE_DAYS
from app.models.JWT import JWT

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=Token, tags=["Auth"])
async def login_for_access_token(request: Request, is_test: Optional[bool] | None = Header(default=False),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    print(f'--> trying to login user {form_data.username}')
    try:
        table_name: str = 'users'
        if is_test:
            table_name = 'usersTest'
        user = authenticate_user(table_name, form_data.username.lower(), form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["name"]}, expires_delta=access_token_expires
        )
        refresh_token_expires = timedelta(days=REFRESH_ACCESS_TOKEN_EXPIRE_DAYS)
        refresh_token = create_access_token(data={"sub": user["name"]}, expires_delta=refresh_token_expires)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/refresh", tags=["Auth"])
async def renew_jwt(request: Request, jwt_token: JWT):
    print(f'--> trying to renew jwt token')
    try:
        token_data = Auth.get_token_payload(jwt_token.token)
        renewed_token = Auth.renew_access_token({"sub": token_data.get("sub")}, ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"token": renewed_token}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
