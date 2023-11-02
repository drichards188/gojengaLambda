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
        sharpe_ratio: float = RiskHandler.handle_get_sharpe_ratio(symbol)
        risk: object = RiskHandler.evaluate_sharpe_ratio(sharpe_ratio)

        if symbol == "btc":
            risk = {"ratio": 1.18, "eval": "Adequate"}
        elif symbol == "eth":
            risk = {"ratio": 0.27, "eval": "Bad"}
        elif symbol == "xrp":
            risk = {"ratio": 0.39, "eval": "Bad"}
        elif symbol == "usdt":
            risk = {"ratio": 0.01, "eval": "Bad"}
        elif symbol == "bnb":
            risk = {"ratio": -0.87, "eval": "Bad"}

        print(f'--> risk is: {risk}')
        return {"response": risk}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
