import os

import uvicorn

from app.core.config import settings, ProdSettings
from app.main import app

if os.environ.get("ENV") == "production":
    settings = ProdSettings()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
