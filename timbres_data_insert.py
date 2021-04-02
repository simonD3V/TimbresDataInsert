# coding: utf-8

import yaml
import os
import sys
import subprocess
from subprocess import call
import json
import uuid
import xlrd
# from yaml_functions import *
from ruamel.yaml import YAML


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
    # curl -X POST -H 'Content-Type: application/json' --data '{'email': 'thomas.bottini@cnrs.fr', 'password' : '?Tr;_Q$D2W4#2!aG'}' http://bases-iremus.huma-num.fr/timbres/auth/login
    token_request = system_call(
        "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/auth/login" % (auth_json, url))
    return str(json.loads(token_request)['data']['refresh_token'])


def listeAttribut(sheet, table_name):
    a = []
    for col in range(sheet.ncols):
        a.append((sheet.cell(0, col).value.replace(' ', '_').replace(
            '\'', '-').replace('é', 'e').replace('à', 'a')).lower())
    return a


def update_uuid_yaml(id_object, simple_table, id_uuid_files):

    # en développement
    # (la fonction devra être insérée dans le test des colonnes id dans insert_data_simple_table() )

    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True

    # chargement du fichier
    with open(id_uuid_files) as file:
        data_yaml = yaml.load(file)

   # on souhaite créer une nouvelle uuid à l'id 3 si elle n'existe pas
    try:
        data_yaml[simple_table][id_object]
        print(str(id_object) + ' existe')
        return(next(iter(data_yaml[simple_table][id_object].values())))

    except:
        # l'id n'a pas été enregistrée, on lui créé une uuid et on rajoute le couple dans le .yaml
        print(str(id_object) + " n'existe pas")
        new_uuid = uuid.uuid4()
        new_line = {id_object: str(new_uuid)}
        data_yaml[simple_table].append(new_line)
        with open(id_uuid_files, 'w') as fo:
            yaml.dump(data_yaml, fo)
        return new_uuid


# ----------MAIN----------------------
if __name__ == "__main__":

    email = 'thomas.bottini@cnrs.fr'
    pwd = '?Tr;_Q$D2W4#2!aG'
    url = 'http://bases-iremus.huma-num.fr/timbres'

    token = token_generation(email, pwd, url)
    print(token)

    # mettre à jour les couples ID/UUID

    excel_path = 'structure_projet_timbres.xlsx'
    sheet_names = ['airs',
                   'éditions',
                   'textes_publiés',
                   'références_externes',
                   'thèmes',
                   'timbres',
                   'airs_références_externes',
                   'textes_publiés_thèmes',
                   'textes_publiés_références_exter',
                   'exemplaires_références_externes'
                   ]

    id_uuid_files = 'uuid_data.yml'

    # insérer les données des tables dites "simples" (qui ne sont pas celles de jointures)
    simple_table = sheet_names[:5]

    # update_uuid_yaml(3, simple_table[0], id_uuid_files)

    insert_data_simple_table(excel_path, simple_table,url, token, id_uuid_files)
    
    # insertion test theme
    # uuid_test1 = '6bf6137e-239e-40c9-a723-6e9aa168c90d'
    # print(str(uuid_test1))
    # uuid_test2 = uuid.uuid4()
    # print(uuid_test2)
    # theme = '[{"id" : "%s", "theme" : "antoine", "type" : "patronyme"}, {"id" : "%s", "theme" : "simon", "type" : "patronyme"}]' % (
    #     str(uuid_test1), str(uuid_test2))
    # print(theme)
    # insertion_theme = os.system(
    #     "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/items/themes? access_token=%s" % (theme, url, token))
