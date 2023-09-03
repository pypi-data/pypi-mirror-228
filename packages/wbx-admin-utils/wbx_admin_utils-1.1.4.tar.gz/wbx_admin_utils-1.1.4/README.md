# wbx-admin-utils

## Usage:
Python3 -m wbx_admin_utils [options] command subcommand [parameters]

## Commands list and syntax:
Python3 -m wbx_admin_utils help commands 


## Commands:
- help
  - commands
- group
  - list : list all groups in admin org
  - list-users group_id : list user ids in given group id
  - add-user email group_id : add user email in given group id
  - add-users-in-csv file group_id : add user listed in CSV file in given group id
  - remove-user file group_id : remove user from given group id
  - remove-users-in-csv file group_id : remove users listed in CSV file in given group id
- user
   - delete-user email : delete user
   - delete-users-in-csv file : delete users listed via email address in given CSV file
   - get-voicemail email : dump user voicemail settings in json format
   - add-voicemail email base user email : set user voicemail options based on another user's voicemail settings
   - add-voicemail-from-csv file base user email : set voicemail options based on another user's voicemail settings for all users listed in CSV file 

## Options:
* -t \<token\> Adds access token as a parameter. Will be read from AUTH_BEARER Env Variable by default        

## Examples:
* Python3 -m wbx_admin_utils group list            
* Python3 -m wbx_admin_utils group list-users \<groupid\>