#!/usr/bin/python
#
# load the list of members from trello and the list of registered
# users from the internal DB to compare them
#
# 2017 rsimai@suse.com
#

import urllib, json, ConfigParser, os, requests

config_file = os.environ['HOME']+'/.externaltools'

config = ConfigParser.ConfigParser()
config.read(config_file)
teamid = config.get('trello.com', 'teamid')
extuser = config.get('suse.de', 'user')
extpass = config.get('suse.de', 'pass')
dataserver = config.get('suse.de', 'server')


# fetch all users from the team and store them in list users
def get_members(trello_key, trello_token, teamid):
    members_url = 'https://api.trello.com/1/organizations/'+teamid+'/members?key='+trello_key+'&token='+trello_token
    server = urllib.urlopen(members_url)
    response = json.loads(server.read())
    users = []
    for record in response:
        userid = record['id']
        users.append(userid)
    return(users)

# fetch the registered users
def get_registered_users(extuser, extpass):
    extusers_url = 'https://'+dataserver+'/admin/users/list_user'
    returncode = requests.get(extusers_url , auth=(extuser, extpass))
    #server = urllib.urlopen(extusers_url)
    #response = json.loads(server.read())
    #print response


get_registered_users(extuser, extpass)

