from trello import TrelloClient
import trellokeys as keys
import ipdb
import os

class TrelloTasks():
    def __init__(self):
        client = TrelloClient(keys.api_key,token=keys.oauth_token)
        #get all the boards
        self.boards = client.list_boards()

    #fetch all cards in a list
    def get_cards(self, board_name, list_name):
        board = filter(lambda x: x.name == board_name, self.boards)[0]
        list = filter(lambda x: x.name == list_name, board.all_lists())[0]
        cards = list.list_cards()

        markdown = "# %s / %s\n\n" % (board_name, list_name)

        for card in cards:
            markdown += "* %s\n" % card.name

        markdown += "\n"
        return markdown

if __name__ == '__main__':
    tt = TrelloTasks()
    print(tt.get_cards('tasks', 'Doing'))
    print(tt.get_cards('valencia','matt'))
