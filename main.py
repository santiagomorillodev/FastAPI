from fastapi import FastAPI
from routers.users import router
from service.database import load_database
root = FastAPI()
root.include_router(router)
