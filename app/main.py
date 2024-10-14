from fastapi import FastAPI
from app.routes import nft_routes


app = FastAPI()

app.include_router(nft_routes.router)

# Точка входа для запуска сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
