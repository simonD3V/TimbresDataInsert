# coding: utf-8

import yaml
import os
import json
import uuid

# ---------FUNCTIONS------------------

def uuid_generation(n) :
    list = []
    for i in range (int(n)) :
        u = uuid.uuid4()
        list.append(str(u))
    return list
    

# ----------MAIN----------------------

if __name__ == "__main__":

    email = 'thomas.bottini@cnrs.fr'
    pwd = '?Tr;_Q$D2W4#2!aG'
    auth_json = '{ "email" : "%s", "password" : "%s"}' % (email, pwd)

    url = 'http://bases-iremus.huma-num.fr/timbres'

    # curl -X POST -H 'Content-Type: application/json' --data '{'email': 'thomas.bottini@cnrs.fr', 'password' : '?Tr;_Q$D2W4#2!aG'}' http://bases-iremus.huma-num.fr/timbres/auth/login
    token_request = os.popen(
        "curl -X POST -H 'Content-Type: application/json' --data '%s' %s/auth/login" % (auth_json, url)).read()
    token = str(json.loads(token_request)['data']['refresh_token'])
    # token captured
    print('\ntoken : ' + token)

    # insertion test theme

    uuid_test = uuid.uuid4()
    theme = '{"id" : "%s", "theme" : "antoine", "type" : "patronyme", "textes_publies" : null }' % (uuid_test)
    insertion_theme = os.popen("curl -X POST -H 'Content-Type: application/json' --data '%s' %s/items/themes? access_token=%s" % (theme, url, token))



