import logging
from decimal import *
from fastapi import APIRouter
from opentelemetry import trace

from app.storage.Dynamo import Dynamo

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()


@router.get("/{username}", tags=["User"])
async def get_user(request: Request, username: str, is_test: Optional[bool] | None = Header(default=False),
                   current_user: User = Depends(get_current_active_user)):
        if Lib.detect_special_characters(username):
            raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
        try:
            print(f'--> the oauth user {current_user}')
            user = UserHandler.handle_get_user(username.lower(), is_test)
            return {"response": user}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", tags=["User"])
async def post_user(request: Request, data: User, is_test: Optional[bool] | None = Header(default=False)):
    with tracer.start_as_current_span(
            "post_user",
            context=extract(request.headers),
            attributes={'attr.username': data.name, 'attr.is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        try:
            if Lib.detect_special_characters(data.name):
                raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')

            resp = UserHandler.handle_create_user(data.name, data.password, is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            # todo how to return original error message
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{username}", tags=["User"])
async def put_user(request: Request, username: str, data: User, is_test: Optional[bool] | None = Header(default=False),
                   current_user: User = Depends(get_current_active_user)):
    with tracer.start_as_current_span(
            "put_user",
            context=extract(request.headers),
            attributes={'username': username.lower(), 'attr.is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        if Lib.detect_special_characters(username):
            raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
        try:
            resp = UserHandler.handle_update_user(username.lower(), data.password, is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{username}", tags=["User"])
async def delete_user(request: Request, username: str, is_test: Optional[bool] | None = Header(default=False),
                      current_user: User = Depends(get_current_active_user)):
    with tracer.start_as_current_span(
            "delete_user",
            context=extract(request.headers),
            attributes={'username': username.lower(), 'is_test': is_test},
            kind=trace.SpanKind.SERVER
    ):
        if Lib.detect_special_characters(username):
            raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='please send legal username')
        try:
            resp = UserHandler.handle_delete_user(username.lower(), is_test)
            return {"response": resp}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
