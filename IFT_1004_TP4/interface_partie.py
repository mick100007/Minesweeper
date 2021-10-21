"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
"""
Module contenant la description de la classe InterfacePartie. Un interface est instancié pour jouer une partie du jeu Démineur.

Auteurs:
Camélia Brochu
Jacques Boisclair
Mickaël Valis
"""




from Classement import Classement
from tkinter import Tk, Frame, Button, Label, Entry, Text, CENTER, RAISED, WORD, NSEW, S, filedialog, messagebox, Text
from tableau import Tableau
from bouton_case import BoutonCase
class InterfacePartie(Tk):
    """
    Interface de la partie incluant les modalités de la fenêtre et les boutons.

    Attributs:
        title (str): Nom de la fenêtre
        dictionnaire_boutons (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple (x, y),
                x étant le numéro de la rangée, y étant le numéro de la colonne.
        partie_terminee (bool): Faux tant qu'on à pas cliqué sur une mine ou que victoire n'est pas True
        victoire (bool): Faux tant qu'on a pas découvert tout les cases sans mines
        nombre_de_cases_devoilees (int): Identifie le nombre de case dévoilée jusqu'à présent
        nombre de mines : le nombre de mines d'une nouvelle partie ou d'une partie archivée
        chronomètre : nombre de temps pour une partie
        classement : classement hiérarchiques des durées des parties
    """

    def __init__(self):
        """
        Initialisation de l'interface de la partie
        """
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        # self.geometry('%dx%d+%d+%d' % (500, 500, 400, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid()
        # self.resizable(0,0)

        bouton_frame = Frame(self)
        bouton_frame.grid_columnconfigure(0, weight=1)
        bouton_frame.grid_rowconfigure(0, weight=1)
        bouton_frame.grid(row=0, column=0, sticky=NSEW)

        bouton_nouvelle_partie = Button(
            bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid_rowconfigure(0, weight=1)
        bouton_nouvelle_partie.grid_columnconfigure(0, weight=1)
        bouton_nouvelle_partie.grid(row=0, column=0, sticky=NSEW)

        bouton_instruction = Button(
            bouton_frame, text='Instructions', command=self.instructions)
        bouton_instruction.grid_rowconfigure(0, weight=1)
        bouton_instruction.grid_columnconfigure(0, weight=1)
        bouton_instruction.grid(row=0, column=1, sticky=NSEW)

        bouton_instruction = Button(
            bouton_frame, text='Classement', command=self.voir_classement)
        bouton_instruction.grid_rowconfigure(0, weight=1)
        bouton_instruction.grid_columnconfigure(0, weight=1)
        bouton_instruction.grid(row=0, column=2, sticky=NSEW)

        bouton_quitter = Button(
            bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.grid_rowconfigure(0, weight=1)
        bouton_quitter.grid_columnconfigure(0, weight=1)
        bouton_quitter.grid(row=0, column=3, sticky=NSEW)

        self.cadre = Frame(self, borderwidth=5,
                           background='blue', relief=RAISED)
        self.cadre.grid_rowconfigure(0, weight=1)
        self.cadre.grid_columnconfigure(0, weight=1)
        self.cadre.grid(padx=10, pady=10, sticky=S)

        # Bind fin de partie
        self.cadre.bind("<<partie_termine>>", self.fin_de_partie)

        label_etat_partie = Label(bouton_frame, justify=CENTER, text="")
        label_etat_partie.grid(row=1, column=0)

        self.etat_partie = Label(bouton_frame, justify=CENTER)
        self.etat_partie.grid(row=2, column=0)

        self.etat_label_texte = Label(bouton_frame, text="RESULTAT", background='blue', foreground='white',
                                      border=1, relief=RAISED)
        self.etat_label_texte.grid(row=1, column=0)

        self.nbre_mines = Label(bouton_frame, justify=CENTER)
        self.nbre_mines.grid(row=2, column=1)
        self.mines_label_texte = Label(bouton_frame, text="MINES", background='yellow', foreground='grey',
                                       border=1, relief=RAISED)
        self.mines_label_texte.grid(row=1, column=1)

        self.chrono = Label(bouton_frame, justify=CENTER, text="0")
        self.chrono.grid(row=2, column=2)
        self.chrono_label_texte = Label(bouton_frame, text="CHRONO", background='purple', foreground='white',
                                        border=1, relief=RAISED)
        self.chrono_label_texte.grid(row=1, column=2)

        self.sauvegarder_partie = Button(
            bouton_frame, text="Sauvegarder Partie", bg='yellow', command=self.sauvegarde_partie)

        self.sauvegarder_partie.grid(row=3, column=1)

        self.ouvrir_partie = Button(
            bouton_frame, text="Ouvrir Partie Sauvegardée", command=self.ouvre_partie)
        self.ouvrir_partie.grid(row=3, column=2)

        self.dictionnaire_boutons = {}

        self.tableau_mines = None
        self.partie_terminee = False
        self.victoire = False
        self.chronometre_actif = False

        self.nombre_de_cases_devoilees = 0

    def parametres_tableau(self):
        """
        Les dimensions de l'interface principal sont demandés à l'utilisateur sur un interface secondaire

        Attributes:
            nbres_de_rangees (int): Nombre de rangées du tableau
            nbres_de_colonnes (int): Nombre de colonnes du tableau
            nbres_de_mines (int): Nombre de mines cachées dans le tableau
        """
        tableau_parametres = Tk()
        # tableau_parametres.geometry('%dx%d+%d+%d' % (500, 300, 450, 200))
        tableau_parametres.title("Paramètres de la nouvelle partie")
        tableau_parametres.configure(bg='blue')

        cadre = Frame(tableau_parametres, borderwidth=5,
                      background='blue', relief=RAISED)
        tableau_parametres.grid_columnconfigure(0, weight=1)
        tableau_parametres.grid_rowconfigure(0, weight=1)
        cadre.grid(padx=10, pady=10, sticky=NSEW)

        texte_demande_infos = Label(tableau_parametres, text='Veuillez entrez les informations suivantes pour créer votre tableau',
                                    font=('Helvetica', 16, 'bold'), bg='purple', bd=4, fg='yellow')
        texte_demande_infos.grid(row=0, column=1, sticky=NSEW)
        texte_colonnes = Label(
            tableau_parametres, text='Nombres de colonnes', bg='white')
        texte_colonnes.grid(row=1, column=0, sticky=NSEW)
        texte_rangees = Label(tableau_parametres,
                              text='Nombres de rangees', bg='white')
        texte_rangees.grid(
            row=1, column=1, sticky=NSEW)
        texte_mines = Label(tableau_parametres,
                            text='Nombres de mines', bg='white')
        texte_mines.grid(
            row=1, column=2, sticky=NSEW)

        self.nbres_de_colonnes = Entry(
            tableau_parametres, width=2, justify=CENTER, bg='light yellow')
        self.nbres_de_colonnes.grid_columnconfigure(0, weight=1)
        self.nbres_de_colonnes.grid_rowconfigure(0, weight=1)
        self.nbres_de_colonnes.grid(row=2, column=0, sticky=NSEW)
        self.nbres_de_rangees = Entry(
            tableau_parametres, width=2, justify=CENTER, bg='light yellow')
        self.nbres_de_rangees.grid_rowconfigure(0, weight=1)
        self.nbres_de_rangees.grid_columnconfigure(0, weight=1)
        self.nbres_de_rangees.grid(row=2, column=1, sticky=NSEW)
        self.nbres_de_mines = Entry(
            tableau_parametres, width=2, justify=CENTER, bg='light yellow')
        self.nbres_de_mines.grid_rowconfigure(0, weight=1)
        self.nbres_de_mines.grid_columnconfigure(0, weight=1)
        self.nbres_de_mines.grid(row=2, column=2, sticky=NSEW)
        self.message = Text(tableau_parametres, width=46, height=2,
                            foreground='red', font=('Chicago', 14, 'bold'), wrap=WORD)
        # self.message = Entry(tableau_parametres, width=50, justify=CENTER, bg='light yellow', foreground='red')
        self.message.grid(row=3, column=1, sticky=NSEW)

        button_1 = Button(tableau_parametres, text='Fermer', font=('Chicago', 24, 'bold'), activebackground='yellow',
                          fg='blue', width=10, relief=RAISED, command=tableau_parametres.destroy)
        button_1.grid(row=5, column=1, sticky=NSEW)
        button_2 = Button(tableau_parametres, text='Enregistrer paramètres', font=('Chicago', 24, 'bold'), activebackground='yellow',
                          fg='blue', width=20, relief=RAISED, command=self.dimension_tableau)
        button_2.grid(row=4, column=1, sticky=NSEW)

        tableau_parametres.mainloop()

    def dimension_tableau(self):
        """
        Les dimensions de l'interface secondaire sont appliqué à l'interface principal

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau
            dimension_colonne (int): Nombre de colonnes du tableau
            nombre_mines (int): Nombre de mines cachées dans le tableau
        """

        self.dimension_rangee = self.nbres_de_rangees.get()
        self.dimension_colonne = self.nbres_de_colonnes.get()
        self.nombre_mines = self.nbres_de_mines.get()
        self.message.delete(1.0, 10.0)

        try:
            self.dimension_rangee = int(self.dimension_rangee)
            self.dimension_colonne = int(self.dimension_colonne)
            self.nombre_mines = int(self.nombre_mines)

        except:
            self.message.insert(1.0, "Paramètres non valides. Recommencez!")
            self.vider_parametres()
            return False

        if self.nombre_mines >= (self.dimension_rangee * self.dimension_colonne):
            self.message.insert(
                1.0, "Le nombre de mines dépassent la quantité de cases disponibles. Recommencez")
            self.vider_parametres()
            return False

        else:
            self.tableau_mines = Tableau(
                self.dimension_rangee, self.dimension_colonne, self.nombre_mines)
            self.message.insert(
                1.0, "Les informations entrées sont exactes. Cliquer sur Fermer")
            self.generer_tableau()

    def voir_classement(self):
        """
        Interface de l'affichage du classement
        """
        interface_classement = Tk()
        interface_classement.title("Classement")

        classement = Classement()

        scores = classement.afficher_classement()
        for score in scores:
            texte = Label(interface_classement, text=score)
            texte.pack()

    def generer_tableau(self, archive=False):
        """
        Méthode pour générer les boutons dans le tableau
        """

        for i in range(1, self.dimension_rangee+1):
            for j in range(1, self.dimension_colonne+1):
                bouton = BoutonCase(self.cadre, i, j)
                bouton.grid_rowconfigure(1, weight=1)
                bouton.grid_columnconfigure(1, weight=1)
                bouton.grid(row=i, column=j, sticky=NSEW)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i, j)] = bouton
        self.nbre_mines["text"] = self.nombre_mines

        if not archive:
            self.tableau_mines.initialiser_tableau()

        if self.chronometre_actif:
            self.after_cancel(self.chronometre_actif)

        self.mise_a_jour_chrono()

    def nouvelle_partie(self):
        """
        Les fonctionnalité du bouton "Nouvelle Partie"
        """
        self.partie_terminee = False
        self.nombre_de_cases_devoilees = 0
        self.nbre_mines["text"] = ""
        self.chrono["text"] = "0"
        self.dictionnaire_boutons = {}
        self.etat_partie["text"] = ""
        self.rafraichir_tableau()
        self.parametres_tableau()

    def quitter(self):
        """
        Attend la confirmation de l'utilisateur avant de quitter
        """
        confirmation = messagebox.askyesno(
            "Quitter", "Voulez-vous vraiment quitter la partie ?")

        if confirmation:
            self.destroy()

    def instructions(self):
        """
        Les fonctionnalité du bouton "Instructions"
        """

        messagebox.showinfo(
            "Instructions", "Bonjour à vous jeune démineur.\n"
                            "Pour jouer, cliquez sur Nouvelle Partie.\n"
                            "Insérez le nombre de rangées, colonnes et mines (un total moins élevé que le nombre total de cases).\n"
                            "Puis, cliquez sur Enregistrer Paramètres et fermez la fenêtre.\n"
                            "La partie peut commencer!\n"
                            "Cliquez sur les carrés.\n"
                            "Les chiffres indiquent le nombre de mines avoisinantes.\n"
                            "Si vous cliquez sur toutes les cases qui n'ont pas de mines, vous gagnez!\n"
                            "\n"
                            "Bonne partie!")

    def devoiler_case(self, event):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont reçues en argument.
        Aussi, si cette case n'est voisine d'aucune mine, on dévoile ses voisins.

        Args:
            event: Event tkinter
        """
        # Empêcher de cliquer quand la partie est terminé
        if self.partie_terminee:
            return False

        bouton = event.widget
        rangee_x = bouton.rangee_x
        colonne_y = bouton.colonne_y

        case_devoilee = self.tableau_mines.devoiler_case(rangee_x, colonne_y)

        self.mise_a_jour_tableau()

        if case_devoilee.est_minee or not self.tableau_mines.contient_cases_a_devoiler():
            self.partie_terminee = True
            self.cadre.event_generate("<<partie_termine>>")

    def mise_a_jour_tableau(self):
        """
        Méthode qui met à jour le tableau
        """
        boutons = self.dictionnaire_boutons

        for bouton in boutons.values():

            case = self.tableau_mines.obtenir_case(
                bouton.rangee_x, bouton.colonne_y)
            if case.est_devoilee:
                if case.est_minee:
                    bouton['text'] = "M"
                else:
                    bouton['text'] = case.nombre_mines_voisines

    def fin_de_partie(self, event):
        """
        Méthode qui affiche la victoire ou la défaite
        """

        if self.tableau_mines.contient_cases_a_devoiler():
            self.etat_partie["text"] = "Défaite"
        else:
            self.etat_partie["text"] = "Victoire"
            score = int(self.chrono["text"])
            classement = Classement()
            classement.ajouter_au_classement(score)

        self.afficher_solution()

    def afficher_solution(self):
        """
        Méthode qui dévoile tout le tableau, une fois la partie terminée
        """
        if self.nombre_de_cases_devoilees == self.nombre_mines or self.partie_terminee:
            for i in range(0, self.tableau_mines.dimension_rangee):
                for j in range(0, self.tableau_mines.dimension_colonne):
                    case = self.tableau_mines.obtenir_case(i + 1, j + 1)
                    case.est_devoilee == True

                    if case.est_minee:
                        bouton = self.dictionnaire_boutons[(i + 1, j + 1)]
                        bouton['text'] = "M"
                    else:
                        bouton = self.dictionnaire_boutons[(i + 1, j + 1)]
                        bouton['text'] = case.nombre_mines_voisines

    def rafraichir_tableau(self):
        """
        Méthode qui rafraîchit le statut de partie dans l'interface
        """
        for bouton in self.cadre.winfo_children():
            bouton.destroy()

    def vider_parametres(self):
        """
        Méthode qui éfface les dimensions de partie dans l'interface secondaire
        """
        self.nbres_de_colonnes.delete(0, 10)
        self.nbres_de_rangees.delete(0, 10)
        self.nbres_de_mines.delete(0, 10)

    def mise_a_jour_chrono(self):
        """
        Méthode qui remet à jour le chronomètre
        """
        if(self.partie_terminee):
            return
        chrono_courant = int(self.chrono["text"])
        self.chrono["text"] = str(chrono_courant+1)
        self.chronometre_actif = self.after(1000, self.mise_a_jour_chrono)

    def sauvegarde_partie(self):
        """
        Méthode qui sauvegarde une partie en cours dans un fichier externe

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau
            dimension_colonne (int): Nombre de colonnes du tableau
            nombre_mines (int): Nombre de mines cachées dans le tableau
            cases minées et dévoilées

        Returns:
            fichier texte avec les données str(tuple) des dimensions et mines du tableau sur une ligne
            et état et contenu des cases str(liste) sur une autre ligne
        """
        if(self.partie_terminee):
            return

        self.archive_partie_dimensions = (
            self.dimension_rangee, self.dimension_colonne, self.nombre_mines, int(self.chrono["text"]))
        self.archive_partie_contenu_tableau = []

        for i in range(1, self.dimension_rangee+1):
            for j in range(1, self.dimension_colonne+1):
                case = self.tableau_mines.obtenir_case(i, j)

                if case.est_minee == True:
                    self.archive_partie_contenu_tableau.append('m')

                elif case.est_devoilee == True:
                    self.archive_partie_contenu_tableau.append(
                        case.nombre_mines_voisines)

                elif case.est_devoilee == False:
                    self.archive_partie_contenu_tableau.append('v')

        self.enregistrer_partie = filedialog.asksaveasfile(
            "r", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        self.fichier_d_ecriture_partie = open('archive.txt', 'w')
        self.fichier_d_ecriture_partie.write(
            str(self.archive_partie_dimensions))
        self.fichier_d_ecriture_partie.write('\n')
        self.fichier_d_ecriture_partie.write(
            str(self.archive_partie_contenu_tableau))
        self.fichier_d_ecriture_partie.close()

    def ouvre_partie(self):
        """
        Méthode qui ouvre un fichier externe d'une partie sauvgardée

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau
            dimension_colonne (int): Nombre de colonnes du tableau
            nombre_mines (int): Nombre de mines cachées dans le tableau
            cases minées et dévoilées

        Returns:
            un tuple avec les données des dimensions et mines du tableau
            une liste contenant l'état et le contenu des cases
            lance la méthode "initialisation_partie_sauvegardee"
        """
        import ast
        # ouverture et lecture du fichier de sauvegarde
        self.ouvrir_partie = filedialog.askopenfile(
            "r", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        self.coller_contenu_partie = open('archive.txt', 'r')
        self.contenu = self.coller_contenu_partie.readlines()
        self.coller_contenu_partie.close()

        self.contenu_partie_archivee = []

        # assigne chaque ligne du texte à un élément de la liste self.contenu_partie_archivee
        for line in self.contenu:
            self.contenu_partie_archivee.append(line.strip())

        # assigne chaque élément de la liste à une nouvelle variable
        self.dimensions_tableau_et_mines_archivees = ast.literal_eval(
            self.contenu_partie_archivee[0])
        self.contenu_tableau_de_partie_archive = ast.literal_eval(
            self.contenu_partie_archivee[1])

        self.initialiser_partie_sauvegardee()

    def nouvelle_partie_de_sauvegarde(self, contenu, dimension_rangee, dimension_colonne, nombre_mines):
        """
        Méthode qui rétablit les mines et les cases voilées à leur état lors de la sauvegarde

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau
            dimension_colonne (int): Nombre de colonnes du tableau
            nombre_mines (int): Nombre de mines cachées dans le tableau
            contenu : contenu et état des cases

        Returns:
            les cases qui étaient minées, dévoilées et voilées lors de la sauvegrade
        """
        count = 0
        self.tableau_mines = Tableau(
            dimension_rangee, dimension_colonne, nombre_mines)

        for i in range(1, self.dimension_rangee+1):
            for j in range(1, self.dimension_colonne+1):
                case = self.tableau_mines.obtenir_case(i, j)

                if contenu[count] == 'm':
                    case.est_minee = True
                    case.est_devoilee = False
                elif contenu[count] == 'v':
                    case.est_minee = False
                    case.est_devoilee = False
                else:
                    case.est_minee = False
                    case.est_devoilee = True
                    case.nombre_mines_voisines = contenu[count]
                    self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
                count += 1

    def initialiser_partie_sauvegardee(self):
        """
        Méthode qui initialise le tableau à son état lors de la sauvegarde

        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau
            dimension_colonne (int): Nombre de colonnes du tableau
            nombre_mines (int): Nombre de mines cachées dans le tableau
            dictionnaire_cases: Nombre de cases et leurs attributs
            dictionnaire_boutons : Nombre de boutons et leurs attributs
            nombres_de_cases_devoilees : Nombre de cases qui sont dévoilées
            etat_de_la_partie : Victoire ou défaite
            rafraichir_tableau : Remise d'un canvas vierge de départ

        Returns:
            Affiche l'état de chaque case et bouton lors de la sauvegarde
        """
        self.partie_terminee = False
        self.nombre_de_cases_devoilees = 0
        self.nbre_mines["text"] = ""
        self.dictionnaire_boutons = {}
        self.dictionnaire_cases = 0
        self.etat_partie["text"] = ""
        self.rafraichir_tableau()

        # assignation des données de la partie à des variable
        contenu = self.contenu_tableau_de_partie_archive
        self.dimension_rangee = self.dimensions_tableau_et_mines_archivees[0]
        self.dimension_colonne = self.dimensions_tableau_et_mines_archivees[1]
        self.nombre_mines = self.dimensions_tableau_et_mines_archivees[2]

        chrono = self.dimensions_tableau_et_mines_archivees[3]
        self.chrono["text"] = str(chrono)

        dimension_rangee = self.dimension_rangee
        dimension_colonne = self.dimension_colonne
        nombre_mines = self.nombre_mines
        self.nouvelle_partie_de_sauvegarde(
            contenu, dimension_rangee, dimension_colonne, nombre_mines)

        self.generer_tableau(archive=True)
        self.mise_a_jour_tableau()


if __name__ == "__main__":
    fenetre = InterfacePartie()
    fenetre.mainloop()
