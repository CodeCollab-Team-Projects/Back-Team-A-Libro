from fastapi import FastAPI
from routes.user_routes import user
import uvicorn

app = FastAPI()

app.include_router(user)

@app.get("/")
def home():
    return {"mgs": "hello world"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

