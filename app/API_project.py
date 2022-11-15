import random

from fastapi import FastAPI
from random import randint

app = FastAPI()
player = [{"naam": "aisaacson0", "mmr": 2436, "level": 208}, {"naam": "bnardoni1", "mmr": 3759, "level": 1141},
          {"naam": "jklugman2", "mmr": 1960, "level": 1023}]


@app.get("/percentage")
async def get_player():
    return random.choice(player)
