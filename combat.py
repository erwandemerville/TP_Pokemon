#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

# ======================== VARIABLES GLOBALES =====================================
DEGATS_POISON = 5  # Nombre de PV perdus à chaque tout à cause du poison
DEGATS_DRAINAGE = 5  # Nombre de PV perdus à chaque tout à cause du drainage
# =================================================================================


class CombatError(Exception):
    """ Classe permettant de générer des messages d'erreur.
    Par exemple : CombatError("ERREUR !") """
    def __init__(self, msg):
        self.message = msg


class Combat:
    """ Classe Pokemon.
    Ses attributs sont :
    - Le pokémon du joueur : Un objet de classe Pokemon
    - Le pokémon adversaire : Un objet de classe Pokemon
    - Le numéro du tour _ntour """

    def __init__(self, pokemon_joueur, pokemon_ennemi):
        """ COMPLETER CE CONSTRUCTEUR + AJOUTER L'ATTRIBUT _ntour ET L'INITIALISER A 1 """
        self._pokemon_joueur = pokemon_joueur
        self._pokemon_ennemi = pokemon_ennemi
        self._ntour = 1  # Numéro du tour


    def getNumeroTour(self):
        """ A COMPLETER - Retourne le numéro du tour actuel """
        return self._ntour

    def augmenterTour(self):
        """ A COMPLETER - Augmenter de 1 le numéro du tour """
        self._ntour += 1

    def afficherEtat(self):
        """ Afficher l'état des pokémons (leur nombre de points de vies restants, l'état (normal, poison, etc.))
        COMPLETER LES POINTILLES """
        joueur = self._pokemon_joueur
        ennemi = self._pokemon_ennemi
        print("---------------------------------")
        print("{} : {} PV restants. Etat : {}. Attaque/Défense : {}/{}".format(joueur.getNom(), joueur.getVies(),
                                                                               joueur.getEtat()["nom_etat"],
                                                                               joueur.getAttaque(),
                                                                               joueur.getDefense()))
        print("{} : {} PV restants. Etat : {}. Attaque/Défense : {}/{}".format(ennemi.getNom(), ennemi.getVies(),
                                                                               ennemi.getEtat()["nom_etat"],
                                                                               ennemi.getAttaque(),
                                                                               ennemi.getDefense()))
        print("---------------------------------")

    def activationEffets(self):
        """ Cette fonction vérifie s'il y a eu des altérations d'état sur les pokémons (comme la paralysie, le poison.)
        - S'ils ne sont pas dans leur état normal (empoisonnés, brulés, etc.), activer les effets en conséquence.
        - Diminuer d'un tour la durée restante pour l'état du pokémon.
        ==> A COMPLETER <== """

        pokemons = [self._pokemon_joueur, self._pokemon_ennemi]  # On met les deux pokémons dans une liste
        for pokemon in pokemons:  # Pour chacun des deux pokémons
            if pokemon.getEtat()["nom_etat"] != 'normal':  # On vérifie si l'état du pokémon est "normal"
                if pokemon.getEtat()["nom_etat"] == 'poison':  # On vérifie si le pokémon est empoisonné
                    print("{} souffre du poison et perd {} PV...".format(pokemon.getNom(), DEGATS_POISON))
                    pokemon.baisserVies(DEGATS_POISON)
                if pokemon.getEtat()["nom_etat"] == 'drainage':  # On vérifie si l'énergie du pokémon est drainées
                    print("L'énergie de {} est drainée. Il perd {} PV...".format(pokemon.getNom(), DEGATS_DRAINAGE))
                    pokemon.baisserVies(DEGATS_DRAINAGE)
                if pokemon.getEtat()["nom_etat"] == 'paralysie':  # On vérifie si le pokémon est paralysé
                    print("{} est paralysé. Il ne peut pas attaquer.".format(pokemon.getNom()))

                duree_restante_etat = pokemon.getEtat()["duree_etat"] - 1
                if duree_restante_etat == 0:
                    pokemon.setEtat({"nom_etat": 'normal'})
                else:
                    pokemon.setEtat({"nom_etat": pokemon.getEtat()["nom_etat"], "duree_etat": duree_restante_etat})

    def attaquer(self, attaque, attaquant, cible):
        """ Lance une attaque sur le pokémon cible.
        :param attaque: (dict) Informations sur l'attaque sous forme d'un dictionnaire.
        :param attaquant: (Pokemon) Le pokémon attaquant.
        :param cible: (Pokemon) Pokemon visé par l'attaque.

        On rappelle qu'une attaque peut peut être de la forme :
        {"nom_attaque": "Charge", "degats_attaque": 35} ou
        {"nom_attaque": "Rugissement", "effet_attaque": "attaque-e", "valeur_attaque": 5} pour les attaques à effets."""

        nom_attaque = attaque["nom_attaque"]
        print("{} ATTAQUE {} !!".format(attaquant.getNom(), nom_attaque))
        if len(attaque) == 3:  # Si attaque à effets
            effet_attaque = attaque["nom_effet"]
            valeur_effet = attaque["valeur_effet"]
            if effet_attaque == 'attaque-e':
                cible.baisserAttaque(valeur_effet)
                print("L'attaque de {} diminue.".format(cible.getNom()))
            elif effet_attaque == 'defense-e':
                cible.baisserDefense(valeur_effet)
                print("La défense de {} diminue.".format(cible.getNom()))
            elif effet_attaque == 'attaque+':
                attaquant.augmenterAttaque(valeur_effet)
                print("L'attaque' de {} augmente.".format(attaquant.getNom()))
            elif effet_attaque == 'defense+':
                attaquant.augmenterDefense(valeur_effet)
                print("La défense de {} augmente.".format(attaquant.getNom()))
            elif effet_attaque == 'poison':
                cible.setEtat({"nom_etat": 'poison', "duree_etat": valeur_effet})
                print("L'énergie de {} est drainée pendant {} tours !".format(cible.getNom(), valeur_effet))
            elif effet_attaque == 'drainage':
                cible.setEtat({"nom_etat": 'drainage', "duree_etat": valeur_effet})
                print("{} est empoisonné pendant {} tours !".format(cible.getNom(), valeur_effet))
            elif effet_attaque == 'paralysie':
                cible.setEtat({"nom_etat": 'paralysie', "duree_etat": valeur_effet})
                print("{} est paralysé pendant {} tours ! Il ne peut plus attaquer".format(cible.getNom(),
                                                                                           valeur_effet))
            else:
                CombatError("ERREUR : Type d'attaque {} inconnu !".format(effet_attaque))
        else:  # Si attaque classique (2 éléments dans le dictionnaire attaque)
            puissance_attaque = attaque["degats_attaque"]
            # Les deux lignes suivantes calculent les dégâts infligés par l'attaque en fonction
            # de la puissance de l'attaque, de l'attaque du pokémon attaquant et de la défense du pokémon ciblé.
            # Vous pouvez changer ce calcul si souhaitez changer la manière dont les dégâts sont déterminés
            degats_infliges = (puissance_attaque * attaquant.getAttaque()) / (cible.getDefense() * 2.4 + 1)
            degats_infliges = round(degats_infliges)  # Arrondir à l'entier le plus proche

            cible.baisserVies(degats_infliges)
            print("{} perd {} PV !".format(cible.getNom(), degats_infliges))

    def messageVictoire(self):
        """ Affiche un message en cas de victoire """
        print("Félicitations ! {} est K.O.".format(self._pokemon_ennemi.getNom()))

    def messageDefaite(self):
        """ A COMPLETER """
        print("{} est K.O. Quel dommage !".format(self._pokemon_joueur.getNom()))

    def jouer(self):
        """ FONCTION QUI GERE LE DEROULEMENT DES TOURS.
        La fonction continue de tourner de manière infinie, jusqu'à ce qu'il y ait un gagnant.
        COMPLETER LA FONCTION """
        tour = 0  # On définit variable locale 'tour' qui vaut 0 si c'est le tour du joueur, 1 si c'est celui de l'ennemi
        while True:  # Boucle infinie
            if self._pokemon_joueur.estMort(): # SI LE POKEMON DU JOUEUR EST MORT (compléter)
                self.messageDefaite()
                return False  # On retourne False pour indiquer une défaite
            elif self._pokemon_ennemi.estMort(): # SI LE POKEMON ENNEMI EST MORT (compléter)
                self.messageVictoire()
                return True  # On retourne True pour indiquer une victoire
            else:
                self.afficherEtat()  # Affichage de l'état des pokémons
                self.activationEffets()  # Activation des alterations d'état
                print("TOUR {}".format(self.getNumeroTour()))  # Affichage du numéro du tour
                if tour == 0:
                    if not self._pokemon_joueur.getEtat()["nom_etat"] == 'paralysie':
                        print("C'est à {} de jouer !".format(self._pokemon_joueur.getNom()))
                        attaque = self._pokemon_joueur.choixAttaque()
                        self.attaquer(attaque, self._pokemon_joueur, self._pokemon_ennemi)
                    tour = 1
                else:  # C'est le tour du pokémon adversaire
                    sleep(3)  # Laisser un délai de 3 secondes
                    if not self._pokemon_joueur.getEtat()["nom_etat"] == 'paralysie':
                        print("C'est à {} de jouer.".format(self._pokemon_ennemi.getNom()))
                        sleep(3)
                        attaque = self._pokemon_ennemi.choixAttaqueAleatoire()
                        self.attaquer(attaque, self._pokemon_ennemi, self._pokemon_joueur)
                        sleep(3)
                    tour = 0
                self.augmenterTour()  # Incrémenter le nombre de tours