import random
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import List

import databases
import sqlalchemy



# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./api.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

players = sqlalchemy.Table(
    "players",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("mmr", sqlalchemy.Integer),
    sqlalchemy.Column("level", sqlalchemy.Integer),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlayerCardIn(BaseModel):
    name: str
    mmr: int
    level: int
class PlayerCard(BaseModel):
    id: int
    name: str
    mmr: int
    level: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/players/create", response_model=PlayerCard)
async def create_player(player: PlayerCardIn):
    query = player.insert().values(name=player.name, mmr=player.mmr, level=player.level)
    last_record_id = await database.execute(query)
    return {**player.dict(), "id": last_record_id}



@app.get("/players/all", response_model=List[PlayerCard])
async def return_all_players():
    query = players.select()
    return await database.fetch_all(query)


@app.get("/players/random")
async def return_random_player():
    return random.choice(players)


@app.get("/player/data/{name}")
async def return_specific_player(name: str):
    for player in players:
        if player.get("name") == name:
            return player
