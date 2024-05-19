from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import media_routes, tweet_routes, user_routes
from app.db.models.media_model import Media  # noqa
from app.db.models.tweet_model import Tweet, tweet_likes  # noqa
from app.db.models.user_model import User, user_followers  # noqa


app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        {"result": False, "error_type": "http_error", "error_message": exc.detail},
        status_code=exc.status_code
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        {"result": False, "error_type": "validation_error", "error_message": str(exc.errors())},
        status_code=400,
    )


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        {"result": False, "error_type": "response_error", "error_message": str(exc.errors())},
        status_code=500,
    )

app.include_router(media_routes.router)
app.include_router(tweet_routes.router)
app.include_router(user_routes.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

templates = Jinja2Templates(directory="static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
