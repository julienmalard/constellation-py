# ConstellationPy

Cette librarie offre un client [Constellation](https://reseau-constellation.github.io/constellation)
pour Python. Elle fonctionne en lançant
un [serveur ws Constellation](https://github.com/reseau-constellation/serveur-ws)
local, avec lequel elle gère ensuite la communication par websocket.

## Installation

Vous pouvez installer ConstellationPy avec `poetry` :

`poetry add constellationPy`

... ou bien avec `pip`

`pip install constellationPy`

Si le serveur Constellation n'est pas déjà installé sur votre machine, ConstellationPy l'installera automatiquement pour
vous. Pour ce faire, vous devrez au tout minimum avoir [Node.js](https://nodejs.org/fr/)
installé localement.

## Utilisation

ConstellationPy est une librarie **asyncrone** basée sur [trio](https://trio.readthedocs.io). Étant donné que le serveur
Constellation est fondamentallement asyncrone aussi, c'était la décision naturelle.

Cependant, nous comprenons bien que la grande majorité des utilisatrices et utilisateurs de Python n'ont aucune idée de
ce qu'est la programmation asyncrone, ni aucun goût ou raison de l'apprendre. C'est pour cela que ConstellationPy vous
offre également un IPA syncrone.

> Vous ne savez pas ce que « syncrone » ou « asyncrone » veulent dire ? Ne vous en faites pas
> et utilisez l'IPA syncrone. « Syncrone » est le terme technique pour le style de code « normal » 
> Python que vous connaissez bien. Si vous voulez en savoir plus, 
> [voici](https://adrienjoly.com/cours-nodejs/sync-vs-async.html) une belle présentation de la différence
> entre les deux (en JavaScript).

Attention ! L'IPA syncrone fonctionne bien pour des petites tâches (p. ex., récupérer un ou deux jeux de données), mais
l'IPA asyncrone est beaucoup plus efficace si vous traitez de grands nombre de données ou de requètes à Constellation.
Si vous avez besoin d'accéder beaucoup de différentes bases de données Constellation, peut-être que ça vaudrait la
peine, après tout,
[d'apprendre](https://trio.readthedocs.io/en/stable/tutorial.html) comment utiliser ces drôles de `async` et `await` en
Python.

### IPA syncrone

En premier lieu, nous devons lancer le serveur Constellation. C'est absolument nécessaire, à moins que vous n'aviez déjà
lancé un serveur Constellation
[manuellement](https://github.com/reseau-constellation/serveur-ws/blob/master/README.md#ligne-de-commande), lorsque, par
exemple, vous voulez exécuter plusieurs codes Python qui utilisent Constellaltion en parallèle sans dupliquer le
serveur (oui, c'est bien possible) !

Donc, on commence. La façon la plus sure, c'est d'utiliser un bloc `with`, car celui-ci fermera automatiquement le
serveur une fois que vous aurez terminé avec. **Cette syntaxe permettra aussi au client Constellation de détecter
automatiquement le port auquel il devra se connecter.**

```python
from constellationPy import Serveur, ClientSync

with Serveur():
    client = ClientSync()
    données = client.appelerUneFonction()
    ...

```

Vous pouvez aussi lancer le client Constellation manuellement. Cette option est particulièrement utile si vous voulez 
obtenir les données les plus à jour du réseau.
N'oubliez pas que Constellation est un *réseau* d'utilisatrices et d'utilisateurs comme vous ! Il n'y
a donc pas de « serveur central » Constellation en tant que tel pour garder une copie des données. 
Si les données qui vous intéressent sont sur
l'ordinateur ou le téléphone d'une autre participante au réseau, cela peut prendre un peu de temps
pour que votre nœud local puisse se connecter à la nuée d'autres nœuds Constellation et reçoive
les données les plus récentes. Comme règle générale, le plus longtemps le nœud reste en ligne,
le plus de connexions et de données il obtiendra.

Vous pouvez donc lancer votre nœud local à l'aide de la ligne de commande. Vous pouvez utiliser
n'importe quel port libre (ici 5001). Vous pouvez le laisser rouler aussi longtemps que vous voudrez,
il y se syncronisera automatiquement avec le réseau Constellation.
Tout client pyConstellation que vous lancerez en même temps obtiendra ainsi les données les plus
à jour disponibles.

Note : pour installer Constellation pour la première fois, faites rouler le code suivant une seule
fois sur votre ordinateur :

```python
from constellationPy import mettre_constellation_à_jour

mettre_constellation_à_jour()
```

Vous pourrez ensuite invoquer le serveur Constellation ainsi :
```shell
constl lancer --port 5001 -b
```

Vous ne savez pas quel port mettre ? Lancez tout simplement `constl lancer` et puis Constellation
vous donnera le numéro du port libre qu'elle aura trouvé.

Vu que vous avez déjà lancé votre propre serveur Constellation, vous devrez spécifier le port manuellement dans le client :

```python
from constellationPy import ClientSync

client = ClientSync(port=5001)
...

```

*Note : vous pouvez également spécifier le port du client sur `Client` et `ouvrir_client` (voir ci-dessous).*

### Fonctions disponibles

Toutes* les fonctions de l'IPA (Interface de programmation
d'application) [Constellation](https://github.com/reseau-constellation/ipa) sont disponibles.

*Note : vous pouvez appeler les fonctions Constellation en forme kebab (`ma_fonction`, style Python)
ou bien chameau (`maFonction`, style JavaScript)*. À titre d'exemple :

```python
from constellationPy import ClientSync, Serveur

with Serveur():
    client = ClientSync()

    résultatChameau = client.obtIdOrbite()
    résultat_kebab = client.obt_id_orbite()

    print(résultatChameau == résultat_kebab)
```

Vous pouvez également accéder les sous-objets de Constellation (`profil`, `bds`, `tableaux`, et ainsi de suite) :

```python
from constellationPy import ClientSync, Serveur

with Serveur():
    client = ClientSync()

    client.profil.sauvegarderNom("fr", "moi !")
    client.bds.créerBd("ODbl-1.0")

```

#### Fonctions bien commodes

L'IPA du client Python vous offre aussi quelques fonctions plus commodes qui n'existent pas dans l'IPA original de
Constellation :

```python
from constellationPy import ClientSync, Serveur

id_tableau = "/orbitdb/zdpu..."

with Serveur():
    client = ClientSync()
    données = client.obt_données_tableau(id_tableau)
```

**Quelques points importants**

* Les fonctions plus obscures qui prennent plus qu'une autre fonction comme argument (p.
  ex. `client.suivreBdDeFonction`) ne fonctionnent pas avec le client Python. Ne vous en faites pas. Elles sont obscures
  pour une raison. Laissez-les en paix. Vous avez amplement de quoi vous amuser avec le reste de l'IPA.
* N'utilisez **pas** les paramètres nommés (p. ex., `client.bds.créerBd(licence="ODbl-1.0")`). Ça va
  créer des ennuis. Un `client.bds.créerBd("ODbl-1.0")` tout simple va faire l'affaire. Si ça vous 
  gêne vraiment, dites-nous le et on y travaillera.
* Avec le client syncrone, les fonctions de suivi (voir ci-dessous) doivent être appellées avec une fonction vide (p.
  ex., `lambda: pass` ou bien tout simplemen `fais_rien`) à la place de la fonction de suivi.
* Vous vous demandez où trouver tous ces drôles de « id tableau » pour les bases de données qui vous intéressent ? Il
  s'agit de l'identifiant unique d'un tableau ou d'une base de données, que vous pouvez récupérer lorsque vous créez la
  base de données, ou bien visuellement avec
  l'[appli Constellation](https://reseau-constellation.github.io/constellation)
  (recherchez l'icône lien 🔗).

#### Fonctions de suivi

Constellation, dans sa version asyncrone JavaScript, offre des fonctions qui, plutôt que de rendre le résultat
immédiatement, *suivent* le résultat à travers le temps et vous notifient (selon une fonction que vous choisissez)
chaque fois que le résultat change. La grande majorité des fonctions utiles de l'IPA de Constellation (p.
ex., `client.tableaux.suivreDonnées`) sont de ce genre.

Évidemment, ce comportement n'est pas util dans un programme syncrone. Le client syncrone `ClientSync`
s'occupe donc de vous rendre le résultat, sans tracas. Il vous suffira de passer une fonction vide là où la fonction
originale s'attendait à avoir la fonction de suivi. Par exemple, si l'on appellerait la fonction comme suit dans
Constellation JavaScript,

```javascript
const données = await client.tableaux.suivreDonnées(id_tableau, fSuivi)
```

Ici, en Python, nous ferons ainsi :

```python
from constellationPy import ClientSync, Serveur, fais_rien

id_tableau = "/orbitdb/zdpu..."
with Serveur():
    client = ClientSync()

    mes_données = client.tableaux.suivreDonnées(id_tableau, fais_rien)
```

### IPA asyncrone

L'IPA asyncrone doit être utilisée avec [trio](https://trio.readthedocs.io/). Il a les mêmes fonctions que l'IPA
syncrone, mais dois être invoqué dans un bloc `async with ouvrir_client() as client:`

```python
import trio

from constellationPy import Serveur, ouvrir_client

id_tableau = "/orbitdb/zdpu..."


async def principale():
    with Serveur():
        async with ouvrir_client() as client:
            données = await client.obt_données_tableau(id_tableau)
            ...


trio.run(principale)
```

#### Fonctions de suivi et `une_fois`

Tel que mentionné ci-dessus, la majorité des fonctions utiles de Constellation sont des fonctions de suivi. Nous devons
les appeler avec une fonction qui sera invoquée à chaque fois que le résultat sera mis à jour.

```python
import trio

from constellationPy import Serveur, ouvrir_client

id_tableau = "/orbitdb/zdpu..."


async def principale():
    with Serveur():
        async with ouvrir_client() as client:
            # Suivre les données du réseau pour 15 secondes, et imprimer les résultats au fur et à mesure
            # qu'ils nous parviennent du réseau
            oublier_données = await client.tableaux.suivreDonnées(id_tableau, print)
            await trio.sleep(15)

            oublier_données()  # Maintenant on ne recevra plus les mises à jour des données


trio.run(principale)
```

Mais en Python, il est probable que, au lieu de vouloir suivre le résultat de la fonction à travers le temps, vous
préférerez obtenir les données présentes et puis poursuivre vos analyses. La fonction `une_fois`
vous permet de faire justement celà :

```python
import trio

from constellationPy import Serveur, ouvrir_client, une_fois

id_tableau = "/orbitdb/zdpu..."


async def principale():
    with Serveur():
        async with ouvrir_client() as client:
            # On doit définir une fonction auxiliaire que ne prend que la fonction de suivi
            # en tant qu'argument
            async def f_données(f):
                return await client.tableaux.suivreDonnées(id_tableau, f)

            # La fonction `une_fois` appellera `f_données`, attendra le premier résultat,
            # et nous renverra celui-ci.
            données = await une_fois(f_données, client)

            return données


mes_données = trio.run(principale)
print(mes_données)
```

## Utilisation avancée

Voici un exemple un peu plus avancé. Si vous avez plusieurs coroutines Python que vous voulez exécuter en parallèle avec
Constellation, vous pouvez créer une pouponnière `trio` et la réutiliser pour les deux coroutines en invoquant `Client`
directement.

```python
import trio
from constellationPy import Client

résultats = {}


async def coroutine1(client):
    données = await client.appelerUneFonction()
    résultats["1"] = données


async def coroutine2(client):
    données = await client.appelerUneFonction()
    résultats["2"] = données


async def principale():
    async with trio.open_nursery() as pouponnière:
        async with Client(pouponnière) as client:
            await client.connecter()  # À ne pas oublier ! Sinon je ne suis pas responsable.

            pouponnière.start_soon(coroutine1, client)
            pouponnière.start_soon(coroutine2, client)


trio.run(principale)

print(résultats)
```

Ceci peut aussi être utile avec
les [canaux](https://trio.readthedocs.io/en/stable/reference-core.html#using-channels-to-pass-values-between-tasks)
de `trio` pour communiquer entre les coroutines :

```python
import trio
from constellationPy import Client

id_tableau = "/orbitdb/zdpu..."


async def coroutine_constellation(pouponnière, canal_envoie):
    async with Client(pouponnière) as client:
        await client.connecter()  # À ne pas oublier ! Sinon je ne suis pas responsable.

        données = await client.obt_données_tableau(id_tableau)

        async with canal_envoie:
            await canal_envoie.send(données)


async def une_autre_coroutine(canal_réception):
    async with canal_réception:
        async for message in canal_réception:
            print(message)  # En réalité, faire quelque chose d'asyncrone, comme écrire au disque


async def principale():
    async with trio.open_nursery() as pouponnière:
        canal_envoie, canal_réception = trio.open_memory_channel(0)

        pouponnière.start_soon(coroutine_constellation, pouponnière, canal_envoie)
        pouponnière.start_soon(une_autre_coroutine, canal_réception)


trio.run(principale)
```

### Traitement des erreurs

Vous pouvez aussi initialiser `Client` avec un canal `trio` pour recevoir les erreurs. Si le client ou le serveur
encontre une erreur, celle-ci sera envoyée au canal erreur au lieu de soulever une erreur et d'arrêter exécution du
programme. Cette option peut être utile lorsque vous ne voulez pas qu'une erreur sur une requête arrête toute
l'exécution du logiciel.

```python
import trio

from constellationPy import Serveur, Client


async def coroutine_client(pouponnière, canal_envoie_erreur):
    async with canal_envoie_erreur:
        async with Client(pouponnière) as client:
            await client.connecter(canal_envoie_erreur)  # À ne pas oublier ! Sinon je ne suis pas responsable.
            # Faire quelque chose avec le client


async def coroutine_erreurs(canal_reçoie_erreurs):
    async with canal_reçoie_erreurs:
        async for erreur in canal_reçoie_erreurs:
            print(erreur)  # Où écrire à un fichier log sur le disque...


async def principale():
    with Serveur():
        async with trio.open_nursery() as pouponnière:
            canal_envoie_erreur, canal_reçoie_erreur = trio.open_memory_channel(0)

            pouponnière.start_soon(coroutine_client, pouponnière, canal_envoie_erreur)
            pouponnière.start_soon(coroutine_erreurs, canal_reçoie_erreur)


trio.run(principale)
```