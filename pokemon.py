#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random  # Module random pour générer des valeurs aléatoires (avec random.choice)


class PokemonError(Exception):
    """ Classe permettant de générer des messages d'erreur.
    Par exemple : PokemonError("ERREUR !") """

    def __init__(self, msg):
        self.message = msg


class Pokemon:
    """ Classe Pokemon.
    Ses attributs sont :
    - Son nom : Chaîne de caractères
    - Son ou ses types : Tableau de chaînes de caractères (Exemple : ['Feu'] ou ['Normal', 'Air']
    - Son nombre de points de vies : Entier
    - Son attaque : Entier
    - Sa défense : Entier
    - Son état : Tuple de deux valeurs, exemple : ('normal', 0) ou ('paralysie', 3)
    - Liste de ses attaques sous forme d'un tableau, par exemple : [['Charge', 50], ['Eclaire', 'paralysie', 5]]"""

    def __init__(self, nom, types, pts_vies, attaque, defense, liste_attaques):
        """ CONSTRUCTEUR A COMPLETER """
        self._nom = nom
        self._types = types
        self._pts_vies = pts_vies
        self._attaque = attaque
        self._defense = defense
        self._liste_attaques = liste_attaques
        self._etat = {"nom_etat": "normal"}  # Etat initial (normal)

    # DEFINITION DES GETTERS :
    # Ce sont les fonctions qui permettent de RECUPERER les valeurs des attributs du pokémon.

    def getNom(self):
        """ A COMPLETER - Retourne la valeur de l'attribut _nom """
        return self._nom

    def getVies(self):
        return self._pts_vies

    def getAttaque(self):
        return self._attaque

    def getDefense(self):
        return self._defense

    def getEtat(self):
        return self._etat

    # DEFINITION DES SETTERS :
    # Ce sont les fonctions qui permettent de MODIFIER les valeurs des attributs du pokémon.

    def setEtat(self, nouvel_etat):
        """ A COMPLETER : Modifie la valeur de l'attribut _etat """
        self._etat = nouvel_etat

    def baisserVies(self, nb):
        """ Fonction qui retire "nb" points de vies au nombre de vie du pokémon.
        Deux possibilités :
        - Si le nouveau nombre de pts de vies est inférieur à 0, on met le nombre de points de vies à 0
        - Sinon, le nouveau nombre de pts de vies est la soustraction de l'ancien nombre de pts de vies et de "nb".
        :param nb: (int) Le nombre de points de vies à retirer. """

        if self._pts_vies - nb < 0:
            self._pts_vies = 0
        else:
            self._pts_vies = self._pts_vies - nb

    def baisserAttaque(self, nb):
        """ Même principe que baisserVies() mais pour l'attaque. """
        if self._attaque - nb < 0:
            self._attaque = 0
        else:
            self._attaque = self._attaque - nb

    def baisserDefense(self, nb):
        """ Même principe que baisserVies() mais pour la défense. """
        if self._defense - nb < 0:
            self._defense = 0
        else:
            self._defense = self._defense - nb

    def augmenterVies(self, nb):
        """ Fonction qui ajoute "nb" vies au nombre de vies actuel du Pokémon. """
        self._pts_vies += nb

    def augmenterAttaque(self, nb):
        self._attaque += nb

    def augmenterDefense(self, nb):
        self._defense += nb

    # AUTRES METHODES UTILES

    def estMort(self):
        """ Retourne True si le Pokémon est mort (points de vies à 0), False sinon. """
        return not self.getVies()

    # METHODES RELATIVES AUX ATTAQUES

    def choixAttaqueAleatoire(self):
        """ Retourne les données d'une attaque choisie aléatoirement.
        COMPLETER LES POINTILLES - On souhaite retourner un élément de _liste_attaques aléatoire).
        """

        attaque = random.choice(self._liste_attaques)
        return attaque

    def choixAttaque(self):
        """ Fonction qui affiche la liste des attaques ainsi que leurs caractéristiques,
        puis retourne les informations sur l'attaque choisie par le joueur (= un dictionnaire de _liste_attaques).
        COMPLETEZ LES POINTILLES SUR LA DERNIERE LIGNE """

        i = 1
        for el in self._liste_attaques:  # Pour chaque liste de _liste_attaques (donc pour chaque attaque)
            print("{} - {} : ".format(i, el["nom_attaque"]), end='')  # On affiche un numéro puis le nom de l'attaque
            if len(el) == 3:  # 3 éléments, cela signifie qu'il s'agit d'une attaque spécial (poison, paralysie, etc.)
                if el["nom_effet"] == 'attaque-e':
                    print("Diminue de {} l'attaque du pokémon ennemi".format(el["valeur_effet"]))
                elif el["nom_effet"] == 'defense-e':
                    print("Diminue de {} la défense du pokémon ennemi".format(el["valeur_effet"]))
                elif el["nom_effet"] == 'attaque+':
                    print("Augmente de {} l'attaque du pokémon allié".format(el["valeur_effet"]))
                elif el["nom_effet"] == 'defense+':
                    print("Augmente de {} la défense du pokémon allié".format(el["valeur_effet"]))
                elif el["nom_effet"] == 'poison':
                    print("Empoisonne votre adversaire pour {} tours.".format(el["valeur_effet"]))
                elif el["nom_effet"] == 'drainage':
                    print("Draine l'énergie de votre adversaire pour {} tours.".format(el["valeur_effet"]))
                elif el["nom_effet"] == 'paralysie':
                    print("Paralyse votre adversaire pour {} tours.".format(el["valeur_effet"]))
                else:
                    PokemonError("ERREUR : Type d'attaque {} inconnu !".format(el["nom_effet"]))
            else:  # Sinon (2 éléments), il s'agit d'une attaque normale.
                print("Puissance de l'attaque : {}".format(el["degats_attaque"]))

            i += 1

        choix = input("Quelle attaque choisissez-vous ? ")
        return self._liste_attaques[int(choix) - 1]
