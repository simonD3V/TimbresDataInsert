# coding: utf-8

import yaml
import os
import json


# ----------MAIN----------------------

if __name__ == "__main__":

    email = 'thomas.bottini@cnrs.fr'
    pwd = '?Tr;_Q$D2W4#2!aG'
    auth_json = '{ "email" : "%s", "password" : "%s"}' % (email, pwd)

    url = 'http://bases-iremus.huma-num.fr/timbres/auth/login'

    # curl -X POST -H 'Content-Type: application/json' --data '{'email': 'thomas.bottini@cnrs.fr', 'password' : '?Tr;_Q$D2W4#2!aG'}' http://bases-iremus.huma-num.fr/timbres/auth/login
    token_request = os.popen(
        "curl -X POST -H 'Content-Type: application/json' --data '%s' %s" % (auth_json, url)).read()
    token = str(json.loads(token_request)['data']['access_token'])
    # token captured
    print('\ntoken : ' + token)
    