import random 
from fastapi import FastAPI

app = FastAPI()
players = [{'naam': "aisaacson0", "mmr": 2436, "level": 208}, {'naam': "bnardoni1", "mmr": 3759, "level": 1141},
          {'naam': "jklugman2", "mmr": 1960, "level": 1023}]

@app.get("/player")
async def return_random_player():
  return random.choice(players)
@app.get("/players/all")
async def return_all_players():
  return players
@app.get("/player/data/{name}")
async def return_specific_player(name: str):
  for player in players:
     if player.get("naam") == name:
        return players
