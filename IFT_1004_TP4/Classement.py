# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Classement.

Auteurs: Camélia
"""

import bisect
import os


class Classement:

    def __init__(self):
        """ Initialisation d'un objet classement.

            Vérifie si le fichier de classement existe et le crée s'il n'existe pas
        """
        if not os.path.exists("classement.txt"):
            with open("classement.txt", 'w'):
                pass

    def afficher_classement(self):
        """
        Lis le fichier de classement et retourne une liste des scores 

        Returns:
            list: Liste des scores
        """

        fichier_classement = open("classement.txt", "r")

        position = 1
        score_liste = []
        for score in fichier_classement.readlines():
            score_liste.append(str(position)+" : "+score.strip("\n"))
            position += 1

        fichier_classement.close()
        return score_liste

    def ajouter_au_classement(self, nouveau_score):
        """
        Ajoute le score du joueur au classement (Ne conserve que les 10 meilleurs)

        Args:
            nouveau_score: Nouveau score à ajouter
        """
        fichier_classement = open("classement.txt", "r")

        score_liste = []
        for score in fichier_classement.readlines():
            score_liste.append(int(score.strip("\n")))

        fichier_classement.close()
        bisect.insort(score_liste, nouveau_score)

        score_liste = score_liste[:10]

        fichier_classement = open("classement.txt", "w")
        for score in score_liste:
            fichier_classement.writelines(str(score)+"\n")

        fichier_classement.close()


if __name__ == "__main__":
    classement = Classement()

    classement.ajouter_au_classement(35)
