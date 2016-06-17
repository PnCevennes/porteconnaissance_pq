Login
======

* /auth/login
  * Permet l'authentification d'un utilisateur
  * Méthode : POST
  * Paramètres :
    * Login
    * Password
  * Retour :
    * Token d'authentification (en cookie)
    * Objet utilisateur loggé

* /auth/generate_password
  * Regénère le mot de passe d'un utilisateur
  * Méthode : POST
  * Paramètres :
    * Email de l'utilisateur
  * Retour :
    * Nouveau mot de passe
    * + Envoie d'un mail

PQ
======

 * /pq
  * Renvoie en geojson les périmètres de quiétude
  * Méthode : GET
  * Condition : être authentifié
* /pq/communes
  * Revoie la liste des communes du territoire avec leur emprise sous forme d'un json
  * Méthode : GET
  * Condition : être authentifié
* /pq/contact/massifs
  * Renvoie la liste des techniciens avec leur contact pour chaque massif
  * Méthode : GET
  * Condition : être authentifié
* /pq/contact/secteur
  * Renvoie la liste des gardes moniteur avec leur contact pour chaque secteur
  * Méthode :GET
  * Condition : être authentifié
