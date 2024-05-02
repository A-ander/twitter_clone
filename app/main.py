from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import media_routes, tweet_routes, user_routes
from app.db.models.media_model import Media
from app.db.models.tweet_model import Tweet, tweet_likes
from app.db.models.user_model import User, user_followers
# from app.db.models import (  # noqa: F401
#     media_model,
#     tweet_model,
#     user_model,
# )

app = FastAPI()
# Подключаем маршруты
app.include_router(media_routes.router)
app.include_router(tweet_routes.router)
app.include_router(user_routes.router)

# Подключение статических файлов
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Подключение шаблонов Jinja2
templates = Jinja2Templates(directory="static")


# Корневой маршрут для отображения index.html
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
