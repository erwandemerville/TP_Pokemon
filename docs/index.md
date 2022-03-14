# TP Classes - Pokémon

Vous pouvez :

* [Cliquer ici](TP.pdf) pour **accéder** à l'**énoncé du TP** en **PDF**.
* [Cliquer ici](TP_Pokemon.zip) pour **télécharger** le **code à trous** du TP.
* [Cliquer ici](TP_Pokemon_Correction.zip) pour **télécharger** le **corrigé** du TP.
* [Cliquer ici](https://replit.com/@erwandemerville/TP-Classes-Pokemon) pour **tester le code en ligne**.

# Réalisation d'un jeu Pokémon

## Objectif du TP

L'objectif de cette séance est de réaliser, en **Python**, un jeu de type RPG.
En particulier, on s'inspirera du jeu **Pokémon**.

Ce projet sera constitué des fichiers suivants :

* **main.py** - Programme principal permettant l'exécution du jeu
* **jeu.py** - Classe qui gère l'ensemble du jeu et réutilise les autres classes
* **combat.py** - Classe permettant de représenter un combat du jeu
* **pokemon.py** - Classe permettant de représenter les Pokémons

Voici une capture de ce que l'on souhaite obtenir :

![Exécution du jeu](images/console.png){ width=50% }

## Pré-requis

Si nécessaire, vous pouvez relire le cours sur les classes [en cliquant ici](http://www.planeteisn.fr/Structuresdonn%C3%A9es6.html).

Les notions d'**objets**, d'**attributs**, de **méthodes**, de **constructeur** notamment doivent vous être familières.

## Modélisation

Voici une modélisation sous forme de diagramme des différentes classes constituant ce projet :

![Modélisation des classes du jeu](images/Jeu_Pokemon.drawio.png){ width=100% }

**Notes** :

* Les données sur les pokémons sont stockées dans un fichier `pokemons.txt`.

  L'inscription d'un pokémon se fait de la manière suivante :

  ```
  Bulbizarre	Plante,Poison	45	49	49
  Charge,50	Rugissement,attaque-e,5	Vampigraine,drainage,3
  ```

  **Chaque donnée est séparée par une tabulation**.
  La première ligne renseigne les données principales sur le Pokémon : Son **nom**, ses **types**, son **nombre de vies**, son **attaque** et enfin sa **défense**.
  La deuxième ligne contient **les attaques du pokémon**.

  S'il s'agit d'une attaque qui inflige simplement des dégâts, on l'écrit sous la forme :
  `Nom_de_lattaque,puissance` (donc seulement deux éléments)

  S'il s'agit d'une attaque qui n'inflige pas de dégâts mais effectue une autre action, ou inflige une altération d'état, on écrira sous la forme suivante (3 éléments) :
  `Nom_attaque,poison,3 ` : Empoisonnement pendant 3 tours (par exemple)
  `Nom_attaque,attaque+,10` : **Augmenter** de **10** points l'attaque du pokémon **allié**
  `Nom_attaque,defense-e,10` : **Diminuer** de **10** points la défense du pokémon **ennemi**.

  Pour l'instant, il existe :

  * `poison` : Empoisonner l'ennemi
  * `paralysie` : Paralyser l'ennemi
  * `drainage` : Drainer la vie de l'ennemi (même effet que poison)
  * `attaque+, attaque-, defense+, defense-` : Augmenter/Diminuer l'attaque ou la défense
  * `attaque-e, defense-e` : Diminuer l'attaque ou la défense ennemie.
  * Rien ne vous empêche de rajouter de nouveaux effets, si vous vous sentez capable de les rajouter dans le code.

  Les attaques de chaque `Pokemon` seront enregistrées dans l'attribut `_liste_attaques` sous forme d'une **liste de dictionnaires**.
  Par exemple, s'il y a 2 attaques : `[{"nom_attaque": "Charge", "degats_attaque": 35}, {"nom_attaque": "Rugissement", "effet_attaque": "attaque-e", "valeur_attaque": 5}]`

  * La première attaque "Charge" a une **puissance de 35**.
  * La seconde attaque **diminue l'attaque de l'ennemi de 5 points**.

* L'état du pokémon sera stockée sous la forme d'un **dictionnaire**.

  * Initialement, l'attribut `_etat` sera égal à `{"nom_etat": "normal"}` => Cela indique que le pokémon est dans son **état** **normal**.
  * S'il est empoisonné par exemple, `_etat` sera égal à `{"nom_etat": "poison", "duree_etat": 3}` => Empoisonnement **pendant encore 3 tours**. (Même principe pour la **paralysie**, ou le **drainage**).
  
* Vous pouvez **ajouter de nouveaux pokémons** dans le fichier `pokemons.txt`, en respectant bien le format.
  Vous pouvez créer vos propres pokémons ou vous inspirer du pokédex :
  
   <https://www.pokebip.com/pokedex/pokedex_5G_liste_des_pokemon.html>

## Réalisation

Ouvrez le dossier `Projet_Pokemon`.

A l'intérieur, vous trouverez des fichiers pré-remplis, que vous devrez compléter.
Les zones à complétez sont marquées par des pointillés `.........`.

* Pensez à **écrire la docstring** de vos fonctions.
* Certaines fonctions sont **déjà** entièrement **écrites**, et il vous sera dans ce cas demandé d'**écrire la docstring** pour vérifier votre compréhension.
* D'autres fonctions **contiennent uniquement la docstring**, qui vous aidera à écrire le corps de la fonction.
  Lisez bien les docstrings et les commentaires pour vous assurer de bien comprendre le fonctionnement du projet !

---

### Déroulement du jeu

Le jeu, défini dans la classe `Jeu`, se déroule **indéfiniment** et ne s'arrête que si :

* Tous les pokémons du jeu sont morts
* Le nombre de victoires correspond à la valeur de la variable globale NB_VICTOIRES
* Le nombre de défaites correspond à la valeur de la variable globale NB_DEFAITES

Si aucune de ces conditions n'est remplie :

* On demande au joueur de choisir un pokémon parmi les pokémons encore vivants du jeu

* L'adversaire choisit un pokémon de manière aléatoire

* On **lance un combat**.

* A la fin du combat, en cas de victoire, on incrémente la valeur du nombre de victoires,

  en cas de défaite, on incrémente la valeur du nombre de défaites.

* On recommence le même déroulement tant qu'aucune des 3 conditions définies précédemment n'est remplie.

### Déroulement d'un combat

Pour vous aider à comprendre, voici une explication du déroulement d'un combat (méthode `jouer` de la classe `Combat`) :

* On **vérifie** si le pokémon du joueur est **mort**. Si oui, fin du combat, avec un message de défaite.
* Sinon, on **vérifie** si le pokémon de l'ennemi est **mort**. Si oui, **fin du combat, avec message de victoire**.
* Si aucun pokémon n'est mort :
  * On affiche les infos sur les pokémon (points de vies, état, attaque, défense...)
  * On active les effets relatifs aux altérations d'état.
  * Si c'est au tour du joueur, le joueur choisit une attaque.
  * Si c'est au tour du joueur adversaire, l'attaque est choisie aléatoirement.
  * A la fin, on incrémente le nombre de tours

# Questions ?

Si vous avez des remarques ou des questions, vous pouvez me contacter à l'adresse <erwan.demerville.etu@univ-lille.fr>