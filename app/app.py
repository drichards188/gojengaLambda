import uuid
import uvicorn

from fastapi import FastAPI, HTTPException
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from app.routes import helloworld_router, account_router, auth_router, portfolio_router
from app.monitoring import logging_config
from app.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.handlers.exception_handler import exception_handler
from app.handlers.http_exception_handler import http_exception_handler

###############################################################################
#   Application object                                                        #
###############################################################################

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###############################################################################
#   Logging configuration                                                     #
###############################################################################

logging_config.configure_logging(level='DEBUG', service='gojenga', instance=str(uuid.uuid4()))

###############################################################################
#   Error handlers configuration                                              #
###############################################################################

app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

###############################################################################
#   Middlewares configuration                                                 #
###############################################################################

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)


###############################################################################
#   Routers configuration                                                     #
###############################################################################
@app.get("/")
async def root():
    print("---> Hello From Gojenga")
    return {"message": "Hello From Gojenga"}


@app.get("/health")
async def health():
    print("---> Health Check")
    return {"message": "Health Check"}


app.include_router(helloworld_router.router, prefix='/hello', tags=['hello'])
app.include_router(account_router.router, prefix='/account', tags=['account'])
app.include_router(auth_router.router, prefix='/auth', tags=['auth'])
app.include_router(portfolio_router.router, prefix='/portfolio', tags=['portfolio'])

###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
