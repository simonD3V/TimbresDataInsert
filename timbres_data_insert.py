# coding: utf-8

import yaml
import os
import subprocess
from subprocess import call
import json
import uuid

# ---------FUNCTIONS------------------

def uuid_generation(n) :
    list = []
    for i in range (int(n)) :
        u = uuid.uuid4()
        list.append(str(u))
    return list

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    tmp = str(p.stdout.read()).replace('\\n', ' ')
    return tmp[2 : len(tmp) - 1]

def token_generation(email, pwd, url): 
    auth_json = '{ "email" : "%s", "password" : "%s"}' % (email, pwd)
    # curl -X POST -H 'Content-Type: application/json' --data '{'email': 'thomas.bottini@cnrs.fr', 'password' : '?Tr;_Q$D2W4#2!aG'}' http://bases-iremus.huma-num.fr/timbres/auth/login
    token_request = system_call(
        "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/auth/login" % (auth_json, url))    
    return str(json.loads(token_request)['data']['refresh_token'])


# ----------MAIN----------------------

if __name__ == "__main__":

    email = 'thomas.bottini@cnrs.fr'
    pwd = '?Tr;_Q$D2W4#2!aG'
    url = 'http://bases-iremus.huma-num.fr/timbres'

    token = token_generation(email, pwd, url)
    
    # insertion test theme
    uuid_test = uuid.uuid4()
    theme = '{"id" : "%s", "theme" : "antoine", "type" : "patronyme", "textes_publies" : null }' % (uuid_test)
    insertion_theme = os.system("curl -X POST -H 'Content-Type: application/json' --data '%s' %s/items/themes? access_token=%s" % (theme, url, token))
    


