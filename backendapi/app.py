from fastapi import FastAPI
from .routes import shoes

app=FastAPI()
app.include_router(shoes.router)

@app.get("/")
def root():
    """
    Returns the content displayed on the root route
    """
    return {"message":"Welcome"}