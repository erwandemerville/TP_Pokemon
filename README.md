# À Lire

Pour exécuter directement le programme, cliquez sur le bouton **Run** vert en haut.

## Pour le groupe de jeudi matin :
Cette version du code contient quelques modifications par rapport à votre version :
* L'attribut `_etat` de la classe **Pokemon** a été remplacé par un dictionnaire (au lieu d'utiliser un tuple).
    * Au lieu d'avoir par exemple `('normal', 0)`, on a `{"nom_etat": "normal"}`
    * Au lieu d'avoir par exemple `('poison', 3)`, on a `{"nom_etat": "poison", "duree_etat": 3}`

* L'attribut `liste_attaques` de la classe **Pokemon** a été remplacé par une liste de dictionnaires (au lieu d'une liste de listes) :
    * Au lieu d'avoir par exemple<br />
    `[ ['Charge', 35], ['Rugissement', 'defense-e', 5] ]`<br />
    On a : <br />
    `[ {"nom_attaque": "Charge", "degats_attaque": 35}, {"nom_attaque": "Rugissement", "nom_effet": "attaque-e", "valeur_effet": 5} ]`.

L'intérêt est de **simplifier la compréhension** du code.<br />
Pour récupérer par exemple le nom de la **deuxième** attaque d'un Pokemon **pkm**, on écrira `pkm._liste_attaques[1]["nom_attaque"]`au lieu de `pkm._liste_attaques[1][0]`.

## Pour le groupe de jeudi après-midi

Il y avait deux erreurs dans la fonction `choixAttaque`de la classe **Pokemon** :
* À la **première ligne**, vous devez avoir `i = 1`et non pas `i = 0`.
* Au **premier "print"** (troisième ligne), remplacez `el[0]`par `el["nom_attaque"]`.
* La ligne à compléter (la dernière) donne bien : <br />
`return self._liste_attaques[int(choix) - 1]`.


## Pour tout le monde

Dans la classe **Jeu** :
* La fonction `deroulementTour` a été renommée en `deroulementCombat`.
* Une fonction `soignerPokemons`a été ajoutée :
    * Cette fonction est appelée avant chaque combat (dans la fonction `deroulementCombat`) et permet de soigner tous les pokémons non morts,<br />
    c'est à dire de restaurer leurs caractéristiques (pts de vie, attaque, défense) à leur état initial avant le prochain combat.

## Questions ?

Si vous avez des remarques ou des questions, vous pouvez me contacter à l'adresse <erwan.demerville.etu@univ-lille.fr>