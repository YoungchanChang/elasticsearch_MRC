import uvicorn
from fastapi import FastAPI
from app.infrastructure.fastapi import mrc_api

app = FastAPI()

app.include_router(mrc_api.router)

if __name__ == "__main__":
    uvicorn.run(
        "app.infrastructure.fastapi.main:app", host="0.0.0.0", port=5101, reload=True
    )