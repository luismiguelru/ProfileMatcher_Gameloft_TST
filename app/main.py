from fastapi import FastAPI
from app.core.db import init_db
from app.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Profile Matcher Service",
        description="Service for matching player profiles with campaigns (Gameloft technical test)",
        version="1.2.0",
    )
    init_db()
    app.include_router(api_router)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
