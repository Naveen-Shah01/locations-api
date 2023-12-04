from fastapi import FastAPI
from . import models
from .database import engine
from .routers import location,user,auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
import time
from psycopg2.extras import RealDictCursor
import psycopg2


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(location.router)
app.include_router(auth.router)


@app.get("/") 
def read_root():
    return {"Hello": "World"}

# implement a totalviews method or api






