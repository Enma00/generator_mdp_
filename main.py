import json
import random
import string
import subprocess
import tkinter as tk
from tkinter import Label, Entry, Button, Checkbutton, ttk, simpledialog

from cryptography.fernet import Fernet


# Fonction pour déchiffrer un mot de passe haché
def dechiffrer_mot_de_passe(mot_de_passe_hache):
    try:
        f = Fernet(cle_de_chiffrement)
        mot_de_passe_dechiffre_bytes = f.decrypt(mot_de_passe_hache.encode())
        mot_de_passe_dechiffre = mot_de_passe_dechiffre_bytes.decode('utf-8')
        return mot_de_passe_dechiffre
    except:
        return None


# Fonction pour fermer le terminal
def fermer_terminal():
    subprocess.call("taskkill /F /IM cmd.exe", shell=True)


# Insérez votre clé de chiffrement ici (remplacez 'VOTRE_CLE' par votre clé)
cle_de_chiffrement = b'hYRjUIuanro-s-oAejIM7fk7vs6RAym9n3efxNRPv_U='  # Convertir en bytes

# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Générateur et Enregistreur de Mot de Passe")
fenetre.geometry("600x400")

# Créer un gestionnaire d'onglets
onglets = ttk.Notebook(fenetre)

# Créer l'onglet de génération de mot de passe
tab_generer = ttk.Frame(onglets)
onglets.add(tab_generer, text="Générer Mot de Passe")

# Créer l'onglet d'affichage de mots de passe
tab_afficher = ttk.Frame(onglets)
onglets.add(tab_afficher, text="Afficher Mots de Passe")

# Ajouter les onglets
onglets.pack(expand=1, fill="both")

# Onglet de génération de mot de passe
longueur_label = Label(tab_generer, text="Nombre de caractères :")
longueur_label.pack()

longueur_entry = Entry(tab_generer)
longueur_entry.pack()

caracteres_speciaux_var = tk.BooleanVar()
caracteres_speciaux_checkbox = Checkbutton(tab_generer, text="Caractères spéciaux", variable=caracteres_speciaux_var)
caracteres_speciaux_checkbox.pack()


# Fonction pour générer un mot de passe
def generer_mot_de_passe():
    longueur = int(longueur_entry.get())
    caracteres = string.ascii_letters + string.digits

    # Vérifier si la case à cocher des caractères spéciaux est cochée
    if caracteres_speciaux_var.get():
        caracteres += string.punctuation

    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    mot_de_passe_label.config(text="Mot de passe généré : " + mot_de_passe)
    return mot_de_passe


generer_button = Button(tab_generer, text="Générer Mot de Passe", command=generer_mot_de_passe)
generer_button.pack()

mot_de_passe_label = Label(tab_generer, text="")
mot_de_passe_label.pack()


# Fonction pour enregistrer un mot de passe avec un nom personnalisé
def enregistrer_mot_de_passe():
    mot_de_passe_genere = mot_de_passe_label.cget("text").replace("Mot de passe généré : ", "")
    if mot_de_passe_genere:
        nom_mdp = simpledialog.askstring("Nom du Mot de Passe", "Entrez un nom pour le mot de passe :")
        if nom_mdp:
            f = Fernet(cle_de_chiffrement)
            mot_de_passe_hache = f.encrypt(mot_de_passe_genere.encode())
            mot_de_passe_hache_str = mot_de_passe_hache.decode('utf-8')

            # Charger les mots de passe enregistrés depuis le fichier JSON
            try:
                with open("mdp.json", "r") as fichier_mdp:
                    mots_de_passe_enregistres = json.load(fichier_mdp)
            except FileNotFoundError:
                mots_de_passe_enregistres = {}

            # Ajouter le nouveau mot de passe au dictionnaire
            mots_de_passe_enregistres[nom_mdp] = mot_de_passe_hache_str

            # Enregistrer le dictionnaire mis à jour dans le fichier JSON
            with open("mdp.json", "w") as fichier_mdp:
                json.dump(mots_de_passe_enregistres, fichier_mdp, indent=4)

            print(f"Mot de passe enregistré : {nom_mdp}")


enregistrer_button = Button(tab_generer, text="Enregistrer Mot de Passe", command=enregistrer_mot_de_passe)
enregistrer_button.pack()


# Fonction pour supprimer un mot de passe
def supprimer_mot_de_passe():
    nom_mdp = simpledialog.askstring("Supprimer un Mot de Passe", "Entrez le nom du mot de passe à supprimer :")
    if nom_mdp:
        # Charger les mots de passe enregistrés depuis le fichier JSON
        try:
            with open("mdp.json", "r") as fichier_mdp:
                mots_de_passe_enregistres = json.load(fichier_mdp)

            # Vérifier si le nom du mot de passe existe
            if nom_mdp in mots_de_passe_enregistres:
                del mots_de_passe_enregistres[nom_mdp]

                # Enregistrer le dictionnaire mis à jour dans le fichier JSON
                with open("mdp.json", "w") as fichier_mdp:
                    json.dump(mots_de_passe_enregistres, fichier_mdp, indent=4)

                print(f"Mot de passe '{nom_mdp}' supprimé.")
            else:
                print(f"Mot de passe '{nom_mdp}' non trouvé.")

        except FileNotFoundError:
            print("Aucun mot de passe enregistré.")


# Bouton pour supprimer un mot de passe
supprimer_button = Button(tab_afficher, text="Supprimer un Mot de Passe", command=supprimer_mot_de_passe)
supprimer_button.pack()


# Fonction pour afficher les mots de passe en clair dans l'onglet "Afficher Mots de Passe"
def afficher_mots_de_passe():
    # Effacer le contenu précédent
    mots_de_passe_text.delete(1.0, tk.END)

    # Charger les mots de passe enregistrés depuis le fichier JSON
    try:
        with open("mdp.json", "r") as fichier_mdp:
            mots_de_passe_enregistres = json.load(fichier_mdp)

        # Afficher les mots de passe en clair dans le Text Widget
        for nom_mdp, mdp_hache in mots_de_passe_enregistres.items():
            mdp_dechiffre = dechiffrer_mot_de_passe(mdp_hache)
            if mdp_dechiffre:
                mots_de_passe_text.insert(tk.END, f"{nom_mdp} : {mdp_dechiffre}\n")
            else:
                mots_de_passe_text.insert(tk.END, f"{nom_mdp} : Erreur de déchiffrement\n")

    except FileNotFoundError:
        mots_de_passe_text.insert(tk.END, "Aucun mot de passe enregistré.")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")


# Bouton pour afficher les mots de passe
afficher_button = Button(tab_afficher, text="Afficher Mots de Passe", command=afficher_mots_de_passe)
afficher_button.pack()

mots_de_passe_text = tk.Text(tab_afficher, height=10, width=40)
mots_de_passe_text.pack()


# Bouton pour ajouter un mot de passe personnalisé
def ajouter_mot_de_passe_personnalise():
    nom_mdp = simpledialog.askstring("Ajouter un Mot de Passe", "Entrez le nom du mot de passe :")
    if nom_mdp:
        mdp_personnalise = simpledialog.askstring("Ajouter un Mot de Passe", f"Entrez le mot de passe pour {nom_mdp} :")
        if mdp_personnalise:
            f = Fernet(cle_de_chiffrement)
            mot_de_passe_hache = f.encrypt(mdp_personnalise.encode())
            mot_de_passe_hache_str = mot_de_passe_hache.decode('utf-8')

            # Charger les mots de passe enregistrés depuis le fichier JSON
            try:
                with open("mdp.json", "r") as fichier_mdp:
                    mots_de_passe_enregistres = json.load(fichier_mdp)
            except FileNotFoundError:
                mots_de_passe_enregistres = {}

            # Ajouter le nouveau mot de passe au dictionnaire
            mots_de_passe_enregistres[nom_mdp] = mot_de_passe_hache_str

            # Enregistrer le dictionnaire mis à jour dans le fichier JSON
            with open("mdp.json", "w") as fichier_mdp:
                json.dump(mots_de_passe_enregistres, fichier_mdp, indent=4)

            print(f"Mot de passe personnalisé '{nom_mdp}' enregistré.")


# Bouton pour ajouter un mot de passe personnalisé
ajouter_personnalise_button = Button(tab_generer, text="Ajouter un Mot de Passe Personnalisé",
                                     command=ajouter_mot_de_passe_personnalise)
ajouter_personnalise_button.pack(pady=5)  # Ajoute un espace en bas

# Automatiser la fermeture du terminal
fermer_terminal()

# Démarrer la boucle principale de Tkinter
fenetre.mainloop()
