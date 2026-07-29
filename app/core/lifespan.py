from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")

    try:
        db_url = settings.DATABASE_URL

        if not db_url:
                raise Exception("Database URL is missing. Check enviornment variable. Server cannot start.")


        print("All set Application Started")

        yield

    except Exception as e:
                print(f"Startup failed: {e}")
                raise  

    finally:
        print("Lifespan cleanup")