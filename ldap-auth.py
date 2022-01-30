#!/usr/bin/env python3
from os import environ as env
from sys import exit, argv
import yaml
import requests as req

if len(argv) >= 1:
    config_file = argv[1]
else:
    config_file = './ldap-auth.yaml'

try:
    username = env.get('username')
    password = env.get('password')
    auth = { 'username': username, 'password': password }
except Exception as error:
    print(error)
    exit(4)

with open(config_file, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

if not 'auth-url' in config:
    print('FATAL: no auth-url found in config file')
    exit(3)

headers = {}

if 'ldap-url' in config:
    headers['X-LDAP-URL'] = config['ldap-url']

if 'ldap-basedn' in config:
    headers['X-LDAP-BaseDN'] = config['ldap-basedn']

if 'ldap-binddn' in config:
    headers['X-LDAP-BindDN'] = config['ldap-binddn']
  if 'ldap-bindpass' in config:
      headers['X-LDAP-BindPass'] = config['ldap-bindpass']

if 'ldap-template' in config:
    headers['X-LDAP-Template'] = config['ldap-template']

if 'ldap-starttls' in config:
    headers['X-LDAP-StartTLS'] = str(config['ldap-starttls'])

if 'ldap-realm' in config:
    headers['X-LDAP-Realm'] = str(config['ldap-realm'])

res = req.get(config['auth-url'], auth=(username, password), headers=headers)
if res.status_code == 200:
    exit(0)
else:
    exit(1)
