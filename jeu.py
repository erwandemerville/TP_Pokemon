#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pokemon import Pokemon
from combat import Combat
from random import randint

# ======================== VARIABLES GLOBALES =====================================
NB_VICTOIRES = 2  # Nombre de victoires à atteindre pour GAGNER
NB_DEFAITES = 2  # Nombre de défaites à atteindre pour GAME OVER
# =================================================================================

class JeuError(Exception):

    def __init__(self, msg):
        self.message = msg


# ===========================================================================================================
#                                               FONCTION UTILES
# ===========================================================================================================
def getDonneesPokemon():
    """ Lit le fichier "pokemons.txt" et récupère toutes les données sous forme d'une liste de dictionnaires.
    Chaque dictionnaire correspond aux données sur un pokémon. """
    tableau_donnees = []
    with open('pokemons.txt') as f:
        i = 0
        j = 0
        line = f.readline()
        while line:
            if i == 0:
                line = line[0:-1]  # Enlever le '\n' de la fin
                tab = line.split('\t')
                tableau_donnees.append({})
                tableau_donnees[j]["nom"] = tab[0]
                tableau_donnees[j]["types"] = tab[1].split(',')
                tableau_donnees[j]["pts_vies"] = int(tab[2])
                tableau_donnees[j]["attaque"] = int(tab[3])
                tableau_donnees[j]["defense"] = int(tab[4])

                i += 1
            elif i == 1:
                tab = line.split('\t')
                tableau_donnees[j]["l_attaques"] = []
                for k in range(len(tab)):
                    t = tab[k].split(',')
                    dic = {"nom_attaque": t[0]}
                    if len(t) == 2:
                        t[1] = int(t[1])
                        dic["degats_attaque"] = t[1]
                    else:
                        t[2] = int(t[2])
                        dic["nom_effet"] = t[1]
                        dic["valeur_effet"] = t[2]
                    tableau_donnees[j]["l_attaques"].append(dic)
                i += 1
            else:
                i = 0
                j += 1

            line = f.readline()

        return tableau_donnees


def creerPokemons(donnees):
    """ Retourne une liste d'objets POKEMON créées à partir des données donnes passées en argument. """
    listep = []
    for el in donnees:
        listep.append(Pokemon(el["nom"], el["types"], el["pts_vies"], el["attaque"],
                              el["defense"], el["l_attaques"]))
    return listep


# ===========================================================================================================
#                                               CLASSE JEU
# ===========================================================================================================

class Jeu:
    """ Classe Pokemon.
    Ses attributs sont :
    - _pokemons : Liste de tous les pokémons créés à partir du fichier pokemons.txt
    - _nb_victoires : Nombre de victoires remportées par le joueur
    - _nb_defaites : Nombre de défaites
    - _nb_combats_joues : Nombre total de combats joués """

    def __init__(self):
        donnees = getDonneesPokemon()
        self._pokemons = creerPokemons(donnees)
        self._nb_victoires = 0
        self._nb_defaites = 0
        self._nb_combats_joues = 0

        jeu_fini = False
        while not jeu_fini:  # Tant qu'on a pas atteint le nombre de victoires ou de défaites spécifié
            if self.getNbVictoires() == NB_VICTOIRES:
                print("BRAVO ! VOUS AVEZ GAGNE !")
                jeu_fini = True  # Fin du jeu
            elif self.getNbDefaites() == NB_DEFAITES:
                print("GAME OVER ! Vous avez perdu trop de combats...")
                jeu_fini = True  # Fin du jeu
            else:
                self.deroulementCombat()

    # DEFINITION DES GETTERS

    def getNbVictoires(self):
        """ Retourne le nombre de victoires remportées par le joueur. """
        return self._nb_victoires

    def getNbDefaites(self):
        """ Retourne le nombre de défaites remportées par le joueur. """
        return self._nb_defaites

    def getNbCombatsJoues(self):
        """ Retourne le nombre total de combats joués. """
        return self._nb_combats_joues

    # -----

    # DEFINITION DES SETTERS

    def ajouterVictoire(self):
        """ Ajoute 1 victoire au nombre de victoires. """
        self._nb_victoires += 1

    def ajouterDefaite(self):
        """ Ajoute 1 victoire au nombre de défaites. """
        self._nb_defaites += 1

    def ajouterCombatJoue(self):
        """ Ajoute 1 victoire au nombre de combats joués. """
        self._nb_combats_joues += 1

    # -----

    def pokemonAleatoire(self, pokemon_deja_choisi):
        """ Retourne un pokémon choisi aléatoirement dans la liste _pokemons, parmi ceux encore en vie.
        De plus, on s'assure de ne pas retourner un pokémon déjà choisi par le joueur.
        :param pokemon_deja_choisi: (str) Nom du pokémon choisi par le joueur """

        tab_vivants = [pkm for pkm in self._pokemons if not pkm.estMort() and not pkm.getNom() == pokemon_deja_choisi]
        if tab_vivants:
            return tab_vivants[randint(0, len(tab_vivants) - 1)]
        else:
            JeuError("Erreur : Il n'y a plus assez de pokémons disponibles pour jouer.")

    def choixPokemon(self):
        """ Fonction qui :
        - Affiche la liste des pokémons encore vivants
        - Demande à l'utilisateur de choisir le pokémon avec lequel il souhaite combattre
        Ce pokémon est ensuite retourné. """

        print("Liste des pokémons encore vivants : \n")
        trouve = False
        for i in range(len(self._pokemons)):  # On parcourt le tableau des pokémons _pokemons
            if not self._pokemons[i].estMort():  # Si le pokémon n'EST PAS MORT
                trouve = True
                print("{} : {}".format(i + 1, self._pokemons[i].getNom()))

        if not trouve:
            JeuError("Erreur : Il n'y a plus assez de pokémons disponibles pour jouer.")
        else:
            choix = input("Entrez le numéro du pokemon que vous souhaitez utiliser : ")
            return self._pokemons[int(choix) - 1]

    def soignerPokemons(self):
        """ Fonction permettant de restaurer les caractéristiques (pts de vie, état, attaque, défense...)
        de tous les pokémons encore en vie à leur état initial. """

        with open('pokemons.txt') as f:
            i = 0
            j = 0
            line = f.readline()
            while line:
                if i == 0:
                    if not self._pokemons[j].estMort():
                        line = line[0:-1]  # Enlever le '\n' de la fin
                        tab = line.split('\t')
                        pts_vies = int(tab[2])
                        attaque = int(tab[3])
                        defense = int(tab[4])
                        self._pokemons[j]._pts_vies = pts_vies
                        self._pokemons[j]._attaque = attaque
                        self._pokemons[j]._defense = defense
                        self._pokemons[j].setEtat({"nom_etat": "normal"})

                    i += 1
                elif i == 1:
                    i += 1
                else:
                    i = 0
                    j += 1

                line = f.readline()


    def deroulementCombat(self):
        self.soignerPokemons()
        pokemon_joueur = self.choixPokemon()
        pokemon_adversaire = self.pokemonAleatoire(pokemon_joueur.getNom())

        print("LANCEMENT DU COMBAT NUMERO {}".format(self.getNbCombatsJoues() + 1))
        combat = Combat(pokemon_joueur, pokemon_adversaire)
        resultat_combat = combat.jouer()
        if resultat_combat:  # En cas de victoire
            self.ajouterVictoire()
        else:
            self.ajouterDefaite()
        self.ajouterCombatJoue()
