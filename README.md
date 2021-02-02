# Porté à connaissance des périmètres de quiétude

Outil de consultation des données relatives aux périmètres de quiétude du Parc National des Cévennes. Cet outil est à destination des collectivités ayant adhérées à la charte.

Les deux objectifs de ce porté à connaissance sont de permettre aux élus locaux référents de: 
- prendre en compte ces périmètres de quiétude dans l’élaboration de la règlementation circulation communale, 
- de contacter l’établissement s’ils ont connaissance d’un projet qui concerne un périmètre de quiétude. Ce contact permettra d’instaurer un dialogue entre porteur de projet et Parc pour concilier au mieux enjeux de protection et réalisation du projet.

Technologies
------------

- Langages : Python, HTML, JS, CSS
- BDD : PostgreSQL, PostGIS
- Serveur : Debian ou Ubuntu
- Framework Python : Flask
- Framework JS : AngularJs
- Framework carto : Leaflet

Architecture
------------
![Schéma architecture](docs/img/shema_architecture.png?raw=true "Schéma architecture")


Installation
------------
### Prérequis 
Python3, Bower
npm install -g bower

### Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 

### Frontend
cd static/
bower install

### Configuration

cp config.py.sample config.py
cp data/maps.json.sample data/maps.json


API
------------
  - Documentation sur les routes : [api](docs/api.md)

License
-------

* OpenSource - GPL V3
* Copyleft 2016 - Parc national des Cévennes

![Logo PnC](static/img/logo_pnc_orange_r.png)


