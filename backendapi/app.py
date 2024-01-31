from fastapi import FastAPI
from .routes import redis_shoes,elastic_shoes

app=FastAPI()
app.include_router(redis_shoes.router)
app.include_router(elastic_shoes.router)

@app.get("/")
def root():
    """
    Returns the content displayed on the root route
    """
    return {"message":"Welcome"}