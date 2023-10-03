from fastapi import FastAPI
from db.database import Base, engine
import endpoints.routes as routes


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(routes.router, tags=["Admin management"], prefix="/api/admin")
