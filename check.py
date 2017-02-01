#!/usr/bin/python

import urllib, json, ConfigParser

#Config = ConfigParser.ConfigParser()
#Config.read("~/.trellochecker")


trello_key = ""
trello_token = ""
teamid = "4e70fbb834cec71bda0ba6dc"



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

# fetch board admins for a specific board
#def get_board_admins(trello_key, trello_token, boardid, teamid):
#    boardadmin_url = 

# fetch all boards owned by team and their members
def get_boards(trello_key, trello_token, teamid):
    boards_url = 'https://api.trello.com/1/organizations/'+teamid+'/boards?key='+trello_key+'&token='+trello_token+'&fields=memberships,name,shortUrl&filter=open'
    server = urllib.urlopen(boards_url)
    response = json.loads(server.read())
    return(response)

# check board members on their team member status
def get_external_users(trello_key, trello_token, userid, teamid):
    user_url = 'https://api.trello.com/1/members/'+userid+'/?fields=idOrganizations,fullName,username,email&key='+trello_key+'&token='+trello_token
    server = urllib.urlopen(user_url)
    response = json.loads(server.read())
    username = response['username']
    fullname = response['fullName']
    organizations = response['idOrganizations']
    status = "ext"
    for org in organizations:
        if org == teamid:
            status = "OK"
    return(username, fullname, status)

users = get_members(trello_key, trello_token, teamid)

all_boards = get_boards(trello_key, trello_token, teamid)

for board in all_boards:
    members = board['memberships']
    url = board['shortUrl']
    boardname = board['name']
    for user in members:
        userid = user['idMember']
        if userid in users:
            continue
        username, fullname, status = get_external_users(trello_key, trello_token, userid, teamid)
        if status == "ext":
            print boardname, url, username, fullname, status

    



