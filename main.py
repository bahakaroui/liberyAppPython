from fastapi import FastAPI
from routes.books import router as books_router
from routes.users import router as users_router
from routes.login import router as login_router
from routes.stats import router as stats_router

from database import create_default_admin
app = FastAPI()
create_default_admin()
app.include_router(users_router)
app.include_router(books_router)
app.include_router(stats_router)
app.include_router(login_router)
@app.get("/")
def read_root():
    return {"Hello": "World"}