from fastapi import FastAPI
from app.routes import nft_routes, auth_routes


app = FastAPI()

app.include_router(nft_routes.router)
app.include_router(auth_routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)