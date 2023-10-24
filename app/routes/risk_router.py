import logging
from fastapi import Request, Header, HTTPException

from fastapi import APIRouter
from starlette import status

from app.handlers.risk_handler import RiskHandler

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/{symbol}", tags=["Risk"])
async def get_sharpe_ratio(request: Request, symbol: str):
    try:
        risk = RiskHandler.handle_get_sharpe_ratio(symbol)
        print(f'--> risk is: {risk}')
        return {"response": risk}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
