# **Welkom!**
> Hallo, in deze readme krijg je een overzicht van wat ik allemaal gedaan heb voor mijn API project.
## **inhoudstafel**
> Hier kan je zien wat je allemaal te wachten staat.

**1.inleiding**

**2.screenshots + uitleg**
## inleiding
> Voor dit project heb ik een API gemaakt met een 1 POST en een aantal GET requests, deze staan ook in verbinding met een database en een webpagina! uitgebreidere beschrijving krijg je in de volgende topics.
> het thema is Rocket League --> hierbij kan je doormiddel van post en get requests oftewel spelers creëeren die dan in de database gezet worden, ofwel vraag je een random speler uit de database. de webpagina beschikt ook over een lijst met alle spelers die er reeds inzitten dat is inderdaad ook een GET request.

## **screenshots + uitleg**
> Ik heb voor dit project veel informatie kunnen halen uit de oefeningen zoals randomizer.py en uit de cursus van API!
laten we beginnen met de repositories die ik heb gebruikt en dan overlopen we wat er allemaal in zit.

>Dit is de repository waar ik mee begonnen ben, de repository voor de API, Dockerfile, etc. [klik hier](https://github.com/TimoGoossens/python-api-test.git)

>Dit word gerunned op okteto in een cloud omgeving. [klik hier](https://api-service-timogoossens.cloud.okteto.net/)

>Dit is de repository waar ik mijn webpagina op laat runnen. [klik hier](https://github.com/TimoGoossens/TimoGoossens.github.io.git)

>Je kan mijn webpagina bezoeken op [klik hier](https://timogoossens.github.io/)

```from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import random
import os
import crud
import models
import schemas
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/players/create/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_name(db, name=player.name)
    if db_player:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_player(db=db, player=player)


@app.get("/players/", response_model=list[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players


@app.get("/players/random/", response_model=schemas.Player)
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return random.choice(players)


@app.get("/players/{player_id}", response_model=schemas.Player)
def read_user(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player
```





