from client.fetcher import Fetcher
from client.parser import Parser1
#from client.parser_rpd import Parser2
from database import Database

class Context:
    def __init__(self, database: Database, fetcher: Fetcher, parser1: Parser1, static: tuple[dict, dict]):
        self.database = database
        self.fetcher = fetcher
        self.parser1 = parser1
        self.schedule_tree = static[0]
        self.messages = static[1]
        #self.tree_rpd = static[2]
