# **Welkom!**
> Hallo, in deze readme krijg je een overzicht van wat ik allemaal gedaan heb voor mijn API project.
## **inhoudstafel**
> Hier kan je zien wat je allemaal te wachten staat.

**1.inleiding**

**2.screenshots + uitleg**
## inleiding
> Voor dit project heb ik een API gemaakt met een 1 POST en een aantal GET requests, deze staan ook in verbinding met een database en een webpagina! uitgebreidere beschrijving krijg je in de volgende topics.

## **screenshots + uitleg**
> Ik heb voor dit project veel informatie kunnen halen uit de oefeningen zoals randomizer.py en uit de cursus van API!
laten we beginnen met de repositories die ik heb gebruikt en dan overlopen we wat er allemaal in zit.

>Dit is de repository waar ik mee begonnen ben, de repository voor de API, Dockerfile, etc. [klik hier](https://github.com/TimoGoossens/python-api-test.git)

>Dit word gerunned op okteto in een cloud omgeving. [klik hier](https://api-service-timogoossens.cloud.okteto.net/)

![image](https://user-images.githubusercontent.com/91054406/202918244-4d767133-8b5b-432e-9846-09d41f1e1f46.png)
![image](https://user-images.githubusercontent.com/91054406/202918311-970e84b9-9d5d-47f6-a20d-d016f2a1d508.png)

>Dit is de repository waar ik mijn webpagina op laat runnen. [klik hier](https://github.com/TimoGoossens/TimoGoossens.github.io.git)

>Je kan mijn webpagina bezoeken op [klik hier](https://timogoossens.github.io/)

![image](https://user-images.githubusercontent.com/91054406/202918780-1d725fb2-6561-4884-812a-673ae15da4c2.png)
>index.html code

`<html>
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
</html>`





