from fastapi import FastAPI
from .routes import shoes

app=FastAPI()
app.include_router(shoes.router)

@app.get("/")
def root():
    return {"message":"Welcome"}