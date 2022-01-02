import json
import os
import db
#from db import insertdb

folder_path = "../Tickets"

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
        key, value = line.strip().split('=')
        ticket[key.strip()] = value.strip()

    # print(ticket)
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
            # historise les fichiers importés
            file.writelines(filename +"\r")
            # log
            print("Fichier importé : ", filename)
            # Import dans MongoDB
            addticket(path + "\\" + filename)

file.close()
db.closedb()
