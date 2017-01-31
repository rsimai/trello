#!/usr/bin/python

import urllib, json

trello_key = ""
trello_token = ""


boards_url = 'https://api.trello.com/1/organizations/suse/boards?key='+trello_key+'&token='+trello_token+'&fields=memberships,name,shortUrl'

user_url = ""

server = urllib.urlopen(boards_url)
response = json.loads(server.read())

print response

for board in response:
    members = board['memberships']
    name = board['name']
    for member in members:
        print member['idMember'], name

    



