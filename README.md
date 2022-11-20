# **Welkom!**
> Hallo, in deze readme krijg je een overzicht van wat ik allemaal gedaan heb voor mijn API project.
## **inhoudstafel**
> Hier kan je zien wat je allemaal te wachten staat.

**1.inleiding**

**2.screenshots + uitleg**

**3.Eindresultaat**

**4.Slotwoord**

## inleiding
> Voor dit project heb ik een API gemaakt met een 1 POST en een aantal GET requests, deze staan ook in verbinding met een database en een webpagina! uitgebreidere beschrijving krijg je in de volgende topics.
> het thema is Rocket League --> hierbij kan je doormiddel van post en get requests oftewel spelers creëeren die dan in de database gezet worden, ofwel vraag je een random speler uit de database. de webpagina beschikt ook over een lijst met alle spelers die er reeds inzitten dat is inderdaad ook een GET request.

## **screenshots + uitleg**
> Ik heb voor dit project veel informatie kunnen halen uit de oefeningen zoals randomizer.py en uit de cursus van API!
laten we beginnen met de repositories die ik heb gebruikt en dan overlopen we wat er allemaal in zit.

>Dit is de repository waar ik mee begonnen ben, de repository voor de API, Dockerfile, etc. [klik hier voor repo](https://github.com/TimoGoossens/python-api-test.git)

>Dit word gerunned op okteto in een cloud omgeving. [klik hier](https://api-service-timogoossens.cloud.okteto.net/)

>Dit is de repository waar ik mijn webpagina op laat runnen. [klik hier voor repo](https://github.com/TimoGoossens/TimoGoossens.github.io.git)

>Je kan mijn webpagina bezoeken [klik hier](https://timogoossens.github.io/)

>Dit is de code voor mijn API "main.py" hier komt alles samen

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

>Dit is de code voor "crud.py"

```
from sqlalchemy.orm import Session

import models
import schemas


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def get_player_by_name(db: Session, name: str):
    return db.query(models.Player).filter(models.Player.name == name).first()


def get_player_by_mmr(db: Session, mmr: int):
    return db.query(models.Player).filter(models.Player.mmr == mmr).first()


def get_player_by_level(db: Session, level: int):
    return db.query(models.Player).filter(models.Player.level == level).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(name=player.name, mmr=player.mmr, level=player.level)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
```

>Dit is de code voor database.py --> hier ga je connectie maken met de database.

```from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlitedb/sqlitedata.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

>Dit is de code voor "models.py" --> hier zorg je voor de class(es) die je nodig hebt.

```from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# --> deze lijn wordt gebruikt als je meerdere tables hebt en ze een relatie wilt geven

from database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    mmr = Column(Integer)
    level = Column(Integer)
```

>Dit is de code van "schemas.py" --> hier maak je de basemodels.

```from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    mmr: int
    level: int


class PlayerCreate(PlayerBase):
    name: str
    mmr: int
    level: int


class Player(PlayerBase):
    id: int
    name: str
    mmr: int
    level: int

    class Config:
        orm_mode = True
```

> "__init__.py" is een leeg bestand.

>**Dit was de code van de API.**

>Nu gaan we kijken wat er allemaal in de Dockerfile, docker-compose en requirements staat.

>Dit is de code voor "docker-compose.yml" --> ik heb hier versie, naam van service, image, ports, volumes voor de database meegegeven.

```version: "3.9"
services:
 API-service:
  image: timogoossens/python-api-test
  ports:
    - "8000:8000"
  volumes:
  - sqlite_useritems_volume:/code/sqlitedb

volumes:
  sqlite_useritems_volume:
```

>Dit is de Dockerfile --> hier zorg je ervoor dat de database en API gaan runnen met de nodige requirements die men gaan halen uit "requirements.txt".
>De laatste lijn runned de API.

```FROM python:3.10.0-alpine
WORKDIR /code
EXPOSE 8000
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code
RUN mkdir -p /code/sqlitedb
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

>Dit is de requirements.txt file --> hierin worden alle nodige modules ingezet die nodig zijn om de API te laten runnen.

```
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
sqlalchemy==1.4.42
```

>Dan nu de code van de front-end --> hier worden alle front-end zaken voorzien de je allemaal ziet en kan verwezenlijke op de webpagina.

```
<html>
<head>
    <script defer src="https://unpkg.com/alpinejs@3.5.0/dist/cdn.min.js"></script>
    <meta charset="UTF-8">
    <style>
body {
    padding-top: 60px;
    background-image: url('rocketleague.jpeg');
    background-size: cover;
    background-position: center;
}
header {
    border-bottom: black solid;
    text-align: center;

}

#border{
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 50px;
    align-content: center;
    margin: auto;
    height: 600px;
    width: 500px;
    background-color: lavender;
    border: dashed;
    overflow:scroll;
    word-wrap: break-word;
}

</style>
</head>
<body>
<div id="border">
  <script>
    function alpineInstance() {
        return {
            players: {}
        }
    }


</script>
    <header>
<h1>Rocket league</h1>
        </header>
<h2>lijst van alle players</h2>
<h4>(refresh pagina als je de lijst wilt updaten!)</h4>
<ul x-data="alpineInstance()" x-init="fetch('https://api-service-timogoossens.cloud.okteto.net/players/')
  .then(response => response.json())
  .then(data => players = data)">
    <template x-for="ply in players" :key="index">
        <li x-text="ply.name"></li>
    </template>
</ul>
 <h3>klik op de knop om een random speler uit de lijst te tonen</h3>
<div x-data="{
        responsedata: null,
        postname: null,
        postmmr: null,
        postlevel: null,
        postid: null,
        async getData() {
            this.responsedata = await (await fetch('https://api-service-timogoossens.cloud.okteto.net/players/random/')).json();
        },
    }">
    <div>
        <button x-on:click="getData">Send get request</button>
    <dl>
        <dt>name:</dt> <strong x-text="responsedata.name">Placeholder</strong>
        <dt>mmr:</dt><strong x-text="responsedata.mmr">Placeholder</strong>
        <dt>level:</dt><strong x-text="responsedata.level">Placeholder</strong>
        <dt>id:</dt><strong x-text="responsedata.id">Placeholder</strong>
        </dl>
        </div>
    </div>

    <h2>creeër een nieuwe player</h2>
    <div>
<div
    x-data="{
        responsedata: null,
        postname: null,
        postmmr: null,
        postlevel: null,
        async createPost() {
            this.responsedata = await (await fetch('https://api-service-timogoossens.cloud.okteto.net/players/create/', {
              method: 'POST',
              body: JSON.stringify({
                    name: this.postname,
                    mmr: this.postmmr,
                    level: this.postlevel
              }),
              headers: {
                'Content-type': 'application/json; charset=UTF-8',
              },
            })).json();
        },
    }"

>
    <input placeholder="name" type="text" x-model="postname">
    <input placeholder="mmr" type="number" x-model="postmmr">
    <input placeholder="level" type="number" x-model="postlevel">
        <button x-on:click="createPost">create</button>

    <p>name that was inserted: <strong x-text="responsedata.name"></strong></p>
    <p>mmr that was inserted: <strong x-text="responsedata.mmr"></strong></p>
    <p>level that was inserted: <strong x-text="responsedata.level"></strong></p>
</div>
        </div>
    </div>


</body>
</html>
```

### Links

>Mijn GitHub repository voor de API: https://github.com/TimoGoossens/python-api-test.git 

>Mijn GitHub repository voor de front-end: https://github.com/TimoGoossens/TimoGoossens.github.io.git 

>Mijn hosted API link: https://api-service-timogoossens.cloud.okteto.net/ 	

>Mijn hosted front-end link: https://timogoossens.github.io/ 

### Postman

>**GET requests**

![image](https://user-images.githubusercontent.com/91054406/202921077-86e84539-1fe4-48a2-8ea2-939864a11846.png)

![image](https://user-images.githubusercontent.com/91054406/202921124-63564e62-14da-40f3-b917-939423b1f602.png)

![image](https://user-images.githubusercontent.com/91054406/202921157-e417e8e7-2677-4ea3-9882-cab4f934bda3.png)

>**POST request**

>ik weet niet 1 2 3 hoe ik die post op postman moet krijgen maar hier heb je een bewijs uit /docs

![image](https://user-images.githubusercontent.com/91054406/202921468-cc0a9b21-f0d1-44f8-97fa-58a6506af9c8.png)

### **openAPI Docs**

![image](https://user-images.githubusercontent.com/91054406/202921468-cc0a9b21-f0d1-44f8-97fa-58a6506af9c8.png)

![image](https://user-images.githubusercontent.com/91054406/202921614-e277b9fd-c27c-4add-a127-62d381e7ed44.png)

![image](https://user-images.githubusercontent.com/91054406/202921667-cb79a40a-9aa1-4678-b026-f5af33a28738.png)

>POST die ik net gemaakt heb laat ik hier zien... Ik had in totaal 2 spelers en nu zijn er drie want de derde is "Timo".
>Ik heb id 3 ingegeven.

![image](https://user-images.githubusercontent.com/91054406/202921715-fddbf1c3-1497-4da4-b8e1-1d17e7d3d8e5.png)

>**Volledige openAPI Docs**

![image](https://user-images.githubusercontent.com/91054406/202921862-195dfe6b-abb5-4402-aee4-54f58fa1a129.png)

## Eindresultaat

### Webpagina

![image](https://user-images.githubusercontent.com/91054406/202922524-e9d7c397-9c43-4c36-b203-2027b0bd821b.png)

![image](https://user-images.githubusercontent.com/91054406/202922547-7409b2fe-9b41-4bf2-9d72-4e2d6976bbfc.png)

![image](https://user-images.githubusercontent.com/91054406/202922619-72388fa8-34d8-426b-925b-b51c98ae8dd6.png)

>**Bij een refresh zie je dat "Brent" is toegevoegd.**

![image](https://user-images.githubusercontent.com/91054406/202922655-bc7a37fa-39aa-41a0-b88c-ee06df55e678.png)

### Okteto

![image](https://user-images.githubusercontent.com/91054406/202922728-240a703c-4449-4259-aa93-261dfa86a423.png)

![image](https://user-images.githubusercontent.com/91054406/202922754-5073eb8b-166c-433f-9e6e-c956acb3c47f.png)

![image](https://user-images.githubusercontent.com/91054406/202922784-09532f79-b9df-4789-ade3-b98bd428793a.png)


# Slotwoord

>**Het was een zeer leuk project! normaal gezien ben ik niet zo voor programmeren maar nu dat er een combinatie gemaakt is met ccs en een beetje app vindt ik heel tof!
>ik hoop dat het document en deze readme duidelijk zijn.
>bedankt voor uw aandacht!**

>**Timo Goossens**

>**r0891940**

>**2ccs01**
