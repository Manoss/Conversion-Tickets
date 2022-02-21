import json
import os
import db
import re
from datetime import datetime
from pathlib import Path #Gestion des slash et anti-slash selon OS
#from db import insertdb

folder_path = Path("../Tickets")


###################
# Converstion Type
###################
def conversionType(ticket, key, value):
    if key == "HORODATAGE_DEB" or key == "HORODATAGE_FIN" or key == "HORODATAGE" or key =="HORODATAGE_TARE":
        try:
            dt_obj = datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
            ticket[key.strip().lower()] = dt_obj
        except:
            print("Date vide")

    elif key =="STATION" or key =="TYPE" or key =="POSTE" or key =="NUM_WAGON" or key == "TABLIER" or key =="TABLIER_TARE" or key == "PRODUIT_LIBELLE" or key =="CODE_PRODUIT" or key =="PRODUIT" or key =="FIN_CHRGT" or key =="NUM_WAGON_TARE" or key =="NUM_RAME_TARE":
        # Renommage cas produit GPL2
        if key == "PRODUIT":
            key = "produit_libelle"
        # Traitement des String, suppression des espaces
        ticket[key.strip().lower()] = value.strip()
    elif key =="URV_TOPR" or key == "AUTORISATION_TOPR":
        # Traitement des booléen
        value = 1 if value =="OUI" else 0
        ticket[key.strip().lower()] = value
    elif key =="DENSITE" or key =="DUREE":
        ticket[key.strip().lower()] = float(value)
    else:
        # Cas des valeurs à vide. Remplacement par -1
        value = -1 if value == "" else value 
        # Insertion dans le dictionnaire
        ticket[key.strip().lower()] = int(value)
        # print("Key ticket Number : ", int(value))

###################
# Insertion dans MongoDB des tickets
###################
def addticket(filename):
    ticket = {}
    #print("Fichier en cours de traitement : ", filename)
    with open(filename) as f:
        content = f.readlines()
        # Supprime les 3 premières lignes (Titre)
        del content[0:3]
    # Mise en list avec suppression du retour chariot
    for line in content:
        # print("Line : ", line)
        # Test si la ligne est du style clé/valeur (GPL1)
        if '=' in line :
            key, value = line.strip().split('=')
            conversionType(ticket, key, value)
            #ticket[key.strip().lower()] = value.strip()


    print(ticket)
    # Insertion dans MongoDB
    db.insertdb(ticket, collection)



###########################
# Main
###########################

collection = db.connectdb()

###########################
# Arborescence des dossiers
###########################

file = open("Historique import fichiers.txt","w")

for path, dirs, files in os.walk(folder_path):
    for filename in files:
        # Seulement les fichiers se terminant par txt
        if filename.endswith(".txt"):
            # Création du chemin complet avec gestion des / et \ selon OS
            fullpath = Path(path) / Path(filename)
            # historise les fichiers importés
            file.writelines(str(fullpath) +"\r")
            # log
            print("Fichier importé : ", fullpath)
            # Import dans MongoDB
            addticket(fullpath)

file.close()
db.closedb()
