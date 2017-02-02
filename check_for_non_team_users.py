#!/usr/bin/python
# encoding=utf-8
#
# this will report all users and which board they are on if
# the board is owned by the team but the user is not a member
# of this team.
# 2017 rsimai@suse.com
#

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib, json, ConfigParser, os

config_file = os.environ['HOME']+'/.externaltools'

config = ConfigParser.ConfigParser()
config.read(config_file)
trello_key = config.get('trello.com', 'key')
trello_token = config.get('trello.com', 'token')
teamid = config.get('trello.com', 'teamid')


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

# fetch data for one user
def get_user_details(trello_key, trello_token, userid):
    user_url = 'https://api.trello.com/1/members/'+userid+'?fields=username,fullName,url&key='+trello_key+'&token='+trello_token
    server = urllib.urlopen(user_url)
    response = json.loads(server.read())
    username = response['username']
    fullname = response['fullName']
    url = response['url']
    return(username, fullname, url)

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

# cache a list of all known users
users = get_members(trello_key, trello_token, teamid)

# get all boards owned by the team
all_boards = get_boards(trello_key, trello_token, teamid)

# go through boards and determine non team members
for board in all_boards:
    boardadmins = []
    boardexternals = []
    members = board['memberships']
    url = board['shortUrl']
    boardname = board['name']
    report = "no"
    for user in members:
        userid = user['idMember']
        membertype = user['memberType']
        if membertype == 'admin':
            boardadmins.append(userid)
        if userid in users:
            continue
        username, fullname, status = get_external_users(trello_key, trello_token, userid, teamid)
        if status == "ext":
            #print boardname, url, username, fullname, status
            boardexternals.append(username)
            report = "yes"
    if report == 'yes':
        print
        print "Board   :", boardname
        print "URL     :", url
        for external in boardexternals:
            username, fullname, url = get_user_details(trello_key, trello_token, external)
            print "External:", username, fullname, url
        for admin in boardadmins:
            username, fullname, url = get_user_details(trello_key, trello_token, admin)
            print "Admin   :", username, fullname, url


