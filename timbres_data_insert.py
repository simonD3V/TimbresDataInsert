# coding: utf-8

import yaml
import os
import sys
import subprocess
from subprocess import call
import json
import uuid
import xlrd

from yaml_functions import *
from cachemanagement import Cache
import requests

# ---------FUNCTIONS------------------

def uuid_generation(n):
    list = []
    for i in range(int(n)):
        u = uuid.uuid4()
        list.append(str(u))
    return list

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    tmp = str(p.stdout.read()).replace('\\n', ' ')
    return tmp[2: len(tmp) - 1]

def token_generation(email, pwd, url):
    auth_json = '{ "email" : "%s", "password" : "%s"}' % (email, pwd)
    token_request = system_call(
        "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/auth/login" % (auth_json, url))
    return str(json.loads(token_request)['data']['access_token'])

def begin_insertion_simple_table(excel_path, mon_cache, sheet_names, url, token):

    # ouvrir chaque feuille excel
    # 1. on commence par ouvrir les tables dites 'simples'

    book = xlrd.open_workbook(excel_path)

    airs_col = ['id', 'sources_musicales', 'air_normalise', 'surnom_1', 'surnom_2', 'surnom_3', 'surnom_4', 'surnom_5', 'surnom_6', 'surnom_7', 'surnom_8',
                'surnom_9', 'surnom_10', 'surnom_11', 'surnom_12', 'surnom_13', 'surnom_14', 'enregistrement_air', 'notes_critiques_airs', 'sources_information_air']
    editions_col = ['id', 'groupe_ouvrage', 'titre_ouvrage', 'auteur', 'nombre_pieces', 'ville_conservation_exemplaire_1', 'depot_conservation_exemplaire_1', 'prefixe_cote', 'numero_cote',
                    'annee_indiquee', 'annee_estimee', 'format', 'manuscrit_imprime', 'forme_editoriale', 'lieu_edition_indique', 'lieu_edition_reel', 'lieu_source_information', 'editeur_libraire_imprimeur']
    textes_publies_col = ['id', 'edition', 'provenance',
                        'groupe_texte', 'titre', 'sur_l_air_de', 'auteur']
    for s in range(3):
        sheet = book.sheet_by_name(sheet_names[s])
        nbr_post, nbr_patch = 0, 0

        print('Traitement de la table : ' + sheet.name)

        if (sheet.name == 'airs'):
            col = airs_col
            name_table = 'airs'
        if (sheet.name == 'éditions'):
            col = editions_col
            name_table = 'editions'
        if (sheet.name == 'textes_publiés'):
            col = textes_publies_col
            name_table = 'textes_publies'

        for row in range(1, sheet.nrows):
            id_value = int(sheet.cell(row, 0).value)
            mon_cache.get_uuid([name_table, id_value], True)

            # Mise à jour du cache
            current_uuid = mon_cache.get_uuid([name_table, str(id_value)])
            get_object = requests.get(
                url+'/items/' + name_table + '/'+current_uuid+'/?access_token=' + token)
            get_object_json = json.loads(get_object.text)

            # Construction du dict json
            j_dict_str = '{'
            for c in range(0, sheet.ncols):
                attr = (sheet.cell(0, c).value.replace(' ', '_').replace(
                    '\'', '-').replace('é', 'e').replace('à', 'a').replace('è', 'e')).lower()
                
                if (attr in col):
                    if (attr == 'id'):
                        j_dict_str = ''.join(
                            [j_dict_str, '"%s" : "%s",' % (attr, current_uuid)])
                    elif (attr == 'edition' and name_table=='textes_publies') :
                        # cas particulier pour les textes publies : aller chercher l'uuid de l'exemplaire
                        j_dict_str = ''.join(
                            [j_dict_str, '"%s" : "%s",' % (attr, mon_cache.get_uuid(['editions', sheet.cell(row, c).value]))])
                    elif (isinstance(sheet.cell(row, c).value, str)):
                        j_dict_str = ''.join([j_dict_str, '"%s" : "%s",' % (
                            attr, str(sheet.cell(row, c).value.replace('"', '\'').replace('\n', ' ')))])
                    else:
                        j_dict_str = ''.join([j_dict_str, '"%s" : "%s",' % (
                            attr, str(sheet.cell(row, c).value))])
            j_dict_str = j_dict_str[:-1] + '}'
            item = json.loads(j_dict_str)

            if ('data' in get_object_json):
                # ligne déjà dans la base : méthode PATCH
                r = requests.patch(url+'/items/' + name_table + '/' +
                                   current_uuid + '?access_token=' + token, json=item)
                # print(r.text)
                nbr_patch += 1
            else:
                # ligne encore non-insérée dans la base : méthode POST
                r = requests.post(url+'/items/' + name_table +
                                  '/?access_token=' + token, json=item)
                # print(r.text)
                nbr_post += 1

        print(str(nbr_post) + ' lignes insérées dans la table ' + name_table)
        print(str(nbr_patch) + ' lignes mises à jour dans la table ' + name_table)

# ----------MAIN----------------------


if __name__ == "__main__":

    email = 'thomas.bottini@cnrs.fr'
    # pwd = '?Tr;_Q$D2W4#2!aG'
    pwd = '14a32e3e-bc5a-4c7d-83f6-6aea62baaab2'
    url = 'http://bases-iremus.huma-num.fr/timbres'

    token = token_generation(email, pwd, url)
    print("        ________________________")
    print("        |                      |")
    print("        |      Insertion       |")
    print("        |     des données      |")
    print("        |                      |")
    print("        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    print("Connexion à l'API de Directus | Token : " + token)

    excel_path = 'structure_projet_timbres.xlsx'
    sheet_names = ['airs',
                   'éditions',
                   'textes_publiés',
                   'références',
                   'thèmes',
                   'timbres',
                   'airs_références_externes',
                   'textes_publiés_thèmes',
                   'textes_publiés_références_exter',
                   'exemplaires_références_externes'
                   ]

    mon_cache = Cache("fichier-cache.yaml")
    begin_insertion_simple_table(excel_path, mon_cache, sheet_names, url, token)
    mon_cache.bye()

    # id_uuid_files = 'uuid_data.yml'
    # uuid_test2 = uuid.uuid4()

    # theme = {"id": str(uuid_test2), "theme": "Roi de France",
    #          "type": "patronyme"}

    # Exemples pour méthode POST (insertion)

    # r = requests.post(url+'/items/themes?access_token=' + token, json=theme)

    # Exemples pour méthode PATCH (uptdate)

    # r = requests.patch(url+'/items/themes/'+str(uuid_test2)+'?access_token=' + token, json={"theme": "Reine de France"})

    # Exemples pour méthode GET

    # uuid_reine_de_france = "abfc2152-4311-4687-9c05-597bf24d850f"
    # uuid_inexistante = "abfc2152-4311-4687-9c05-597bf24d850d"

    # r = requests.get(url+'/items/themes/'+uuid_reine_de_france+'/?access_token=' + token)
    # j = json.loads(r.text)
