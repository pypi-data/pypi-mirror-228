#!/usr/local/bin/python3

import csv
import requests
import os
# import sys
import json
import logging
import time
import argparse

logging.basicConfig()

parser = argparse.ArgumentParser()

token=""
if ( 'AUTH_BEARER' in os.environ ):
    token = os.environ['AUTH_BEARER']

parser.add_argument("-t", "--token", dest="token", default=token, help="your personal token")
parser.add_argument("-d", "--debug", dest="debug", default=False, help="debug mode")   
parser.add_argument('command', type=str, help='')    
parser.add_argument('subcommand', type=str, help='')    
parser.add_argument('parameters', type=str, nargs='*', help='')    

args = parser.parse_args()

DEBUG=0
if (args.debug):
    DEBUG=int(args.debug)
    if (DEBUG>=3):
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)


#sets the header to be used for authentication and data format to be sent.
def setHeaders():         
    accessToken_hdr = 'Bearer ' + args.token
    spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
    return (spark_header)

def trace(lev, msg):
    if (DEBUG >= lev):
        print(msg)

# print items array fields listed in 'il' 
#
def print_items(il, items):
    for i in il:
        print(i,",", end='', sep='')
    print ("")        
    for item in items:
        for i in il:
            try:
                v=item[i]
            except KeyError:
                v=""
            print (v, ",", end='', sep='')
        print ("")

# returms user id of given user email address 
# returns 0 if not found, -1 if error  
#
def get_user_id(ue):
    header=setHeaders()
    
    trace (3, f"In get_user_id for {ue}")  

    # disable warnings about using certificate verification
    requests.packages.urllib3.disable_warnings()
    get_user_url="https://webexapis.com/v1/people?email=" + ue
    # send GET request and do not verify SSL certificate for simplicity of this example
    r = requests.get(get_user_url, headers=header, verify=True)
    s = r.status_code
    if s == 200 :
        j = r.json()
        if ( len(j["items"]) == 0 ):
            trace (1, f"user email {ue} not found")
            return(0)
        else:
            if ( len(j["items"]) > 1 ):
                trace(1, f"Error found more than one match for user {ue}")
                return(-2)
            if ( len(j["items"]) == 1 ):
                u = j["items"][0]
                trace (3,f"email {ue} found {u['id']} ")
                return(u['id'])     
    else :
        trace(1,f"get_user_id got error {s}: {r.reason}")  
        return(-1)

# lists all groups 
#
def get_grps_list(a):
    #
    url=f"https://webexapis.com/v1/groups"
    r = requests.request("GET", url, headers=setHeaders())
    s = r.status_code
    j = r.json()
    if s == 200 :
        # print(j)
        hl =[ 'id', 'displayName' ]
        print_items ( hl, j["groups"] )
    else:
        print (f"got error {s}: {r.reason}")  

# lists users in given group id 
#
def list_users_in_grp(a):
    gid=a[0]
    url=f"https://webexapis.com/v1/groups/{gid}/Members?startIndex=1&count=500"
    r = requests.request("GET", url, headers=setHeaders())
    s = r.status_code
    j = r.json()
    if s == 200 :
        # print(j)
        hl =[ 'id', 'displayName' ]
        print_items ( hl, j["members"] )
    else:
        trace(1,f"got error {s}: {r.reason}")  


# returns user id for a given email address 
# returns 0 or negative value on failure
#

# Adds/Del user id to given group id 
# returns 1 on success 
#
def uid_to_grp(cmd, uid,gid):

    trace (3, f"In uid_to_grp {cmd}, {uid} , {gid} ")
    header=setHeaders()
    # disable warnings about using certificate verification
    requests.packages.urllib3.disable_warnings()

    url=f"https://webexapis.com/v1/groups/{gid}"
    match cmd:
        case "add":
            body='{"members": [ { "id": "' + uid + '" } ] }'
        case "del":
            body='{"members": [ { "id": "' + uid + '" ,"operation":"delete" } ] }'
        case _:
            trace(1,f"invalid command {cmd}")
            return(-1)

    r = requests.patch(url, headers=header, data=body, verify=True)
    s = r.status_code
    if s == 200 :
        trace(3,f"success")  
        return(1) 
    else:
        print (f"got error {s}: {r.reason}")
        return(-1)
    
# Adds/Del user email to given group id 
# returns 0 on success 
#
def user_to_grp(a):
    (cmd, ue, gid)=(a[0],a[1],a[2])
    uid = get_user_id(ue)
    if (uid):
        r=uid_to_grp(cmd, uid, gid)
        if (r > 0):
            trace(2,f"{cmd} command successful for user {ue}") 
        else:
            trace(1,f"{cmd} command failed for user {ue}") 
    else:
        trace(1,f"Failed to find user email {ue}") 

vm_tmpl = """
{
    "enabled": true,
    "notifications": {
            "enabled": false,
    },
    "sendBusyCalls": {
            "enabled": true,
            "greeting": "DEFAULT"
    },
    "sendUnansweredCalls": {
            "enabled": true,
            "greeting": "DEFAULT",
            "numberOfRings": 3
    },
    "transferToNumber": {
            "enabled": false
    },
"""

# returns json body with VM settings for given user email
# returns -1 on failure 
#
def get_user_vm(a):
    (ue)=(a[0])
    
    trace(3,f"in get_user_vm {a}")

    uid=get_user_id(ue)

    trace(3,f"get_user_vm: got id {uid}")

    if (uid):
        header=setHeaders()
        # disable warnings about using certificate verification
        requests.packages.urllib3.disable_warnings()

        url=f"https://webexapis.com/v1/people/{uid}/features/voicemail"
        r = requests.get(url, headers=header, verify=True)
        s = r.status_code
        if s == 200 :
            d = r.json()
            j=json.dumps(d)
            trace(3, f"success for get_user_vm {ue} : got {j}")  
            return(j)
        else:
            trace(1, f"got error {s}: {r.reason}")  


# Enables VM for given user email with given json body
# returns 1 on success, negative value on failure 
#
def set_user_vm(a):
    (ue)=(a[0])
    (body)=(a[1])

    trace(3,f"in set_user_vm {a}")

    uid=get_user_id(ue)
    if (uid):
        header=setHeaders()
        # disable warnings about using certificate verification
        requests.packages.urllib3.disable_warnings()

        url=f"https://webexapis.com/v1/people/{uid}/features/voicemail"
        r = requests.put(url, headers=header, data=body, verify=True)
        s = r.status_code
        if s == 204 :
            trace(3, f"success")  
            return(1) 
        else:
            trace(1, f"got error {s}: {r.reason}")
            return(-1)
    else:
        trace(1,f"get_user_id {ue} error ") 
        return(-2)

# Enables VM for given user email based on another user email 'template'
# returns set_user_vm status or -1 if base user not found
#
def set_user_vm_based_on_other_user(a):
    (ue, be)=(a[0], a[1])

    trace(3,f"in set_user_vm_based_on_other_user {a}")

    tmpl=get_user_vm([be])
    if ( tmpl ):
        # replace other email with target email
        bdy=tmpl.replace(be, ue)
        a=[ue,bdy]
        return (set_user_vm(a))
    else:
        trace(1,"get_user_vm error")
        return(-1)


# calls given fct for each user in given csv file 
# csv file is the first parameter of the a array 
# the called fucnt parameters are passed via an array containing the rest of the input array a
# exits on file error 
#
def user_csv_command(fct, a):

    trace(3,f"in user_csv_command {fct.__name__} {a}")
    file=a.pop(0)

    header=setHeaders()
    # disable warnings about using certificate verification
    requests.packages.urllib3.disable_warnings()
    
    try:
        csvfile = open(file)
        trace(3,f"{file} open OK")
    except OSError:
        print (f"Could not open file {file}")
        sys.exit()

    with csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ue=row['email']
            a.insert(0, ue)
            r=fct(a)
            if (r>0):
                trace(2,f"{fct.__name__} command successful for user {ue}") 
            else:
                trace(1,f"{fct.__name__} command failed for user {ue}")
            time.sleep(0.1)

################
## GROUPS
################
def add_user_to_grp(a):
    a.insert(0,"add")
    user_to_grp(a)

def del_user_to_grp(a):
    a.insert(0,"del")
    user_to_grp(a)

def add_users_in_csv_to_grp(a):
    a.insert(1,"add")
    user_csv_command(user_to_grp, a)

def del_users_in_csv_to_grp(a):
    a.insert(1,"del")
    user_csv_command(user_to_grp, a)

###############
## USERS
################

# delete user from given email adress
# returns 1 if good   
#
def del_user(a): 
    ue=a[0]
    trace(3,f"in delete_user {a}")

    uid=get_user_id(ue)
    if (uid): 
        url=f"https://webexapis.com/v1/people/{uid}"
        r = requests.request("DELETE", url, headers=setHeaders())
        s = r.status_code
        if s == 204 :
            trace (2, f"User {ue} deleted ")
            return(1)
        else:
            trace(1,f"del_user : Error {s}")  
            trace(1,r.text.encode('utf8'))
            return(-1)
    else:
        trace (1, f"del_user: {ue} not found")  
        return(-1)

def uf_del_user(a):
    if (del_user(a) > 0):
        print (f"User {a[0]} successfully deleted")  
    else:
        print (f"Error. User {a[0]} not deleted")  


def del_users_in_csv(a):
    user_csv_command(del_user,a)

def reset_users(a): 
    print("WIP")

def add_vm(a): 
    set_user_vm_based_on_other_user(a)

def add_vm_csv(a): 
    user_csv_command(add_vm, a)


###############
## syntax
################

def print_help(a): 
    print("Here is some help")

def print_syntax(): 
    for cmd in syntax:
        print(cmd)
        for scmd in syntax[cmd]:
            params=syntax[cmd][scmd]['params']
            hlp=syntax[cmd][scmd]['help']
            print("   " + scmd + ' ' + " ".join(params) + " : " + hlp )

syntax = { 
    "group" : {
        # "help":                 {"params":["command"],"fct":print_help},
        "list":                 {"params":[],"fct":get_grps_list, "help":"list all groups in admin org"},
        "list-users":           {"params":["group_id"],"fct":list_users_in_grp, "help":"list user ids in given group id"},
        "add-user":             {"params":["email", "group_id"],"fct":add_user_to_grp, "help":"add user email in given group id"},
        "add-users-in-csv":     {"params":["file", "group_id"],"fct":add_users_in_csv_to_grp, "help":"add user listed in CSV file in given group id"},
        "remove-user":          {"params":["email", "group_id"],"fct":del_user_to_grp, "help":"remove user email from given group id"},
        "remove-users-in-csv":  {"params":["file", "group_id"],"fct":del_users_in_csv_to_grp, "help":"remove users listed in CSV file in given group id"}, 
    },
    "user" : { 
        # "help":                  {"params":[],"fct":print_help},
        # "reset-access":          {"params":["email"],"fct":reset_users, "help":"reset user access token"},
        "delete-user":           {"params":["email"],"fct":uf_del_user, "help":"delete user "},
        "delete-users-in-csv":   {"params":["file"],"fct":del_users_in_csv, "help":"delete users listed via email address in given CSV file"},
        "get-voicemail":         {"params":["email"],"fct":get_user_vm, "help":"dump user voicemail settings in json format"},
        "add-voicemail":         {"params":["email", "base user email"],"fct":add_vm, "help":"set user voicemail options based on another user's voicemail settings "},
        "add-voicemail-from-csv":{"params":["file", "base user email"],"fct":add_vm_csv, "help":"set voicemail options based on another user's voicemail settings for all users listed in CSV file"},
    }
}


def main():

    # print(args)

    # first 2 params are commands
    #
    (cmd1, cmd2) = (args.command, args.subcommand )

    if cmd1 not in syntax:
        print ("Command [" + cmd1 + "] is invalid")
        print_syntax()
        exit()

    if cmd2 not in syntax[cmd1]:
        print ("Command [" + cmd2 + "] is invalid")
        print_syntax()
        exit()

    # check param count
    #
    par_arr=syntax[cmd1][cmd2]['params']
    if (len(args.parameters) == len(par_arr)):
        # call function associated with command 
        fct=syntax[cmd1][cmd2]['fct']
        fct(args.parameters)
    else:
        print("Incorrect parameters. Check syntax ")
        print_syntax()
    #
   
main()


