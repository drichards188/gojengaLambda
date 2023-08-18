import logging
from typing import Optional

from fastapi import APIRouter, Request, Header, Depends, HTTPException
from opentelemetry import trace
from opentelemetry.propagate import extract
from starlette import status

from app.models.Portfolio import Portfolio
from app.common.Auth import get_current_active_user, User
from app.common.Lib import Lib
from app.handlers.portfolio_handler import PortfolioHandler

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()


@router.get("/{username}", tags=["Portfolio"])
async def get_portfolio(request: Request, username: str, is_test: Optional[bool] | None = Header(default=False),
                        current_user: User = Depends(get_current_active_user)):
    with tracer.start_as_current_span(
            "get_portfolio",
            context=extract(request.headers),
            attributes={'attr.username': username.lower(), 'attr.is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        if Lib.detect_special_characters(username):
            raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
        try:
            account = PortfolioHandler.handle_get_portfolio(username.lower(), is_test)
            return {"response": account}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", tags=["Portfolio"])
async def post_account(request: Request, data: Portfolio, is_test: Optional[bool] | None = Header(default=False),
                       current_user: User = Depends(get_current_active_user)):
    with tracer.start_as_current_span(
            "post_account",
            context=extract(request.headers),
            attributes={'attr.username': data.username, 'attr.is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        try:
            if Lib.detect_special_characters(data.username):
                raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')

            resp = PortfolioHandler.handle_create_portfolio(data.username, data, is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{username}", tags=["Portfolio"])
async def put_user(request: Request, username: str, data: Portfolio,
                   update_type: Optional[str] = Header(None),
                   is_test: Optional[bool] | None = Header(default=False),
                   current_user: User = Depends(get_current_active_user)):
    with tracer.start_as_current_span(
            "post_account",
            context=extract(request.headers),
            attributes={'attr.username': data.username, 'attr.is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        try:
            if Lib.detect_special_characters(data.username):
                raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')

            resp = PortfolioHandler.handle_update_portfolio(data.username, data, is_test, update_type)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{username}", tags=["Portfolio"])
async def delete_user(request: Request, username: str, is_test: Optional[bool] | None = Header(default=False),
                      current_user: User = Depends(get_current_active_user)):
    with tracer.start_as_current_span(
            "delete_portfolio",
            context=extract(request.headers),
            attributes={'username': username.lower(), 'is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        if Lib.detect_special_characters(username):
            raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
        try:
            resp = PortfolioHandler.handle_delete_portfolio(username.lower(), is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
