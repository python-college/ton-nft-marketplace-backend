from fastapi import FastAPI
from app.routes import auth_routes, management_routes


app = FastAPI(root_path="/main")

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(management_routes.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
