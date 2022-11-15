from fastapi import FastAPI
import random

app = FastAPI()


# uvicorn randomizer:app --reload
# http://127.0.0.1:8000/

@app.get("/percentage")
async def read_user_me():
    num = random.randint(0, 100)
    return {"percentage": num}