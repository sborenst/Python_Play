#https://pypi.python.org/pypi/py-trello/0.9.0
#pip install py-trello

import requests
import json
from pprint import pprint
import csv
import sys

################################################################################

key = ''
# if you're storing your key in this file, you don't need the following three lines
if not key:
  from settings import trello_key
  key = trello_key

token = ''
# if you're storing your token in this file, you don't need the following three lines
if not token:
  from settings import trello_token
  token = trello_token

params_key_and_token = {'key':key,'token':token}
base = 'https://api.trello.com/1/'

################################################################################
################################################################################
################################################################################

def main(argv):
    parse_args(argv)
    global card_desc
    global csv_file
    global card_name

    board_id = get_board_id(board_name)
    if board_id:
        print("Found board: " + board_name + ", id:" + board_id)
    else:
        print("Could not find board:" + board_name + ", Creating Board")
        board_id = create_trello_board(board_name)

    listid = get_first_list_id(board_name)
    print("get_first_list_id:", listid)
    print("csv_file is:", csv_file)




    try:
        card_name
    except NameError:
        card_name = "Default card name"
        print("No Card name provided")
    else:
        try:
            card_desc
        except NameError:
            card_desc = "Default card description"
            print("No Card desc provided")
        create_single_trello_card(listid,card_name, card_desc )

    try:
        csv_file
    except NameError:
        csv_file = "Default card name"
        print("No csv_file provided")
    else:
        print("Creating trellos cards from csv")
        create_tello_cards_from_csv(listid,csv_file)



def get_first_list_id(board_name):
    board_id = get_board_id(board_name)
    print ("board_id is:",board_id)

    # apiquery = {'fields': 'id', 'lists': 'open'}
    params=dict(params_key_and_token)
    # params.update(apiquery)
    lists_url = base + '/boards/' + board_id + '/lists'
    # Send out request and register the answer in "response"
    response = requests.get(lists_url, params=params)
    # save the answer into our boards dictionary
    lists = response.json()
    return lists[0]['id']

def get_board_id(board_name):
    apiquery = {'fields': 'name', 'lists': 'open'}
    params=dict(params_key_and_token)
    params.update(apiquery)
    boards_url = base + 'members/me/boards'
    # Send out request and register the answer in "response"
    response = requests.get(boards_url, params=params)
    # save the answer into our boards dictionary
    boards = response.json()

    for board in boards:
        if board['name'] == board_name:
            print("found board ",board['name'])
            return board['id']
    return False

################################################################################
################################################################################
################################################################################

def create_single_trello_card(listid,card_name,card_desc):
        cards_url = base + 'cards'
        arguments = {'name': card_name,
                     'desc': card_desc,
                     'idList' : listid }
        response = requests.post(cards_url, params=params_key_and_token, data=arguments)

def create_trello_board(board_name):
        boards_url = base + 'boards'
        arguments = {'name': board_name,
                     'desc': 'Board created by python',
                     'defaultLists' : 'true' }
        response = requests.post(boards_url, params=params_key_and_token, data=arguments)
        print(response.text)
def create_tello_cards_from_csv(listid,csv_file):

        # Read CSV File
        cards_url = base + 'cards'
        tickets = csv.DictReader(open(csv_file,'rb'), delimiter='|' )
        for ticket in tickets:
            if ticket['Effort']:
                name = ticket['Name'] + "(" + ticket['Effort'] + ")"
            else:
                name = ticket['Name']
            description = ticket['Description']
        # Let's provide a name and description for the card
            arguments = {'name': name,
                         'desc': description,
                         'idList' : listid }
            response = requests.post(cards_url, params=params_key_and_token, data=arguments)




def parse_args(argv):
    import getopt

    try:
      opts, args = getopt.getopt(argv,"hf:b:c:d:",["file=","board=","card=","desc="])
    except getopt.GetoptError:
      print sys.argv[0] +' -f <inputfile> -b "board" -c "card"'
      sys.exit(2)
    for opt, arg in opts:
        pprint(arg)
        if opt == '-h':
            print sys.argv[0] +' -f <inputfile> -b "board" -c "card"'
            sys.exit()
        elif opt in ("-f", "--file"):
            global csv_file
            csv_file = arg
        elif opt in ("-b", "--board"):
            global board_name
            board_name = arg
        elif opt in ("-c", "--card"):
            global card_name
            card_name = arg
        elif opt in ("-d", "--desc"):
            global card_desc
            card_desc = arg

if __name__ == "__main__":
   main(sys.argv[1:])

# For the full documentation, see https://trello.com/docs/
# if debug:
#     print("response url is", response.url)
#     print("Available Boards are:")
#     for board in boards:
#       print(' '*5 + board['name'])
