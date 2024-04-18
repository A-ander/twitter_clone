from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import media_routes, tweet_routes, user_routes

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
