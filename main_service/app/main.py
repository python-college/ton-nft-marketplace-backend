from fastapi import FastAPI
from app.routes import nft_routes, auth_routes, management_routes


app = FastAPI(root_path="/main")

app.include_router(nft_routes.router)
app.include_router(auth_routes.router)
app.include_router(management_routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
