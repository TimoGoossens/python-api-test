import random
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class API_base(BaseModel):
    name: str
    mmr: int
    level: int


player1 = {"name": "aisaacson0", "mmr": 2436, "level": 208}
player2 = {"name": "bnardoni1", "mmr": 3759, "level": 1141}
player3 = {"name": "jklugman2", "mmr": 1960, "level": 1023}

players = [player1, player2, player3]

ply1 = {0: player1}
ply2 = {0: player2}
ply3 = {0: player3}


@app.get("/players/all")
async def return_all_players():
    return players


@app.get("/players/random")
async def return_random_player():
    return random.choice(players)


@app.get("/player/data/{name}")
async def return_specific_player(name: str):
    for player in players:
        if player.get("name") == name:
            return player
