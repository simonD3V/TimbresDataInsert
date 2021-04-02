# coding: utf-8

import yaml
import os
import subprocess
from subprocess import call
import json
import uuid
import xlrd
from yaml_functions import *

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


def insert_data_simple_table(excel_path, simple_table, url, token, id_uuid_files):
    
    # essai test pour les airs
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_name(simple_table[0])

    airs_col = listeAttribut(sheet, simple_table[0])
    json_str = '['
    for row in range(1, sheet.nrows):
        json_str = ''.join([json_str, '{'])
        for col in range(sheet.ncols):
            # if col = 'id'
                # id = sheet.cell(row, col).value
                # update_uuid_yaml(id, simple_table[0], id_uuid_files) 
            if (isinstance(sheet.cell(row, col).value, str)):
                json_str = ''.join([json_str, '"%s" : "%s",' % (
                    # cellules très modifiées 
                    airs_col[col], str(sheet.cell(row, col).value.replace('"', '\'').replace('(', '').replace(')', '').replace("'", ' ')))])
            else:
                json_str = ''.join([json_str, '"%s" : "%s",' % (
                    airs_col[col], str(sheet.cell(row, col).value))])
            if (col == sheet.ncols-1):  
                json_str = json_str[:-1]
                json_str = ''.join([json_str, '},'])
    json_str = json_str[:-1]
    json_str = ''.join([json_str, ']'])
    print(json_str)
    insertion_airs = os.system(
        "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/items/airs? access_token=%s" % (json_str, url, token))

def update_uuid_yaml(id_object, simple_table, id_uuid_files) :

    # en développement 
    # (la fonction devra être insérée dans le test des colonnes id dans insert_data_simple_table() )

    # chargement du fichier
    with open(id_uuid_files) as file:
        data_yaml = yaml.load(file, Loader=yaml.FullLoader)
    
    # on souhaite créer une nouvelle uuid à l'id 3 si elle n'existe pas 
    try :
        data_yaml[simple_table][id_object]
        print(str(id_object) + ' existe')
        
    except :
        # l'id n'a pas été enregistrée, on lui créé une uuid et on rajoute le couple dans le .yaml
        print(str(id_object) + " n'existe pas")
        new_uuid = uuid.uuid4()
        print(new_uuid)
        new_line = [{simple_table:{id_object:str(new_uuid)}}]
        print(new_line)
        # update_yaml = yaml.dump(new_line, file, default_flow_style=False)


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

    update_uuid_yaml(3, simple_table[0], id_uuid_files) 


    #insert_data_simple_table(excel_path, simple_table, url, token, id_uuid_files)

    # insertion test theme
    # uuid_test1 = uuid.uuid4()
    # uuid_test2 = uuid.uuid4()
    # theme = '[{"id" : "%s", "theme" : "antoine", "type" : "patronyme", "textes_publies" : null }, {"id" : "%s", "theme" : "simon", "type" : "patronyme", "textes_publies" : null }]' % (
    #     uuid_test1, uuid_test2)
    # insertion_theme = os.system(
    #     "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/items/themes? access_token=%s" % (theme, url, token))
