from fastapi import FastAPI
from routes.user import user
from routes.books import book
from config.database import engine, Base
import uvicorn

app = FastAPI()

app.include_router(user, prefix="/users", tags=["users"])
app.include_router(book, prefix="/books", tags=["books"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mgs": "Success"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

