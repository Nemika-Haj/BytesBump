from pymongo import MongoClient
from core.files import Data

client = MongoClient(Data('config').yaml_read()['mongo'])

class Servers:
    def __init__(self, server=None):
        self.server = server
        self.col = client["BytesBump"]["servers"]
        self.prefixes = client["BytesBump"]["prefixes"]

    def get(self):
        return self.col.find_one({"_id":self.server})
    
    def get_all(self):
        return self.col.find({})

    """
    Add a server to the database.
    Expected params: Desc, Color, Listing, WebhookID
    """

    def add(self, **params):
        params['_id'] = self.server
        self.col.insert_one(params)

    """
    Update a server in the database.
    """
    
    def update(self, **checks):
        self.col.update_one({
            "_id": self.server
        }, {
            "$set": params
        })

    """
    Remove a server from the database.
    """
    
    def delete(self, **checks):
        if self.server:
            self.col.delete_one({'_id': self.server})
        else:
            self.col.delete_one(checks)

    """
    Prefix management
    """

    @property
    def hasPrefix(self):
        r = self.prefixes.find_one({'_id':self.server})
        if r: return True
        return False

    @property
    def deletePrefix(self):
        self.prefixes.delete_one({'_id':self.server})

    def setPrefix(self, prefix):
        if self.hasPrefix: self.prefixes.update_one({'_id':self.server}, {'$set':{'prefix':prefix}})
        else: self.prefixes.insert_one({'_id':self.server, 'prefix':prefix})

    def getPrefix(self):
        prefix = self.prefixes.find_one({'_id':self.server})
        if prefix: return prefix["prefix"]
        else: return Data("config").yaml_read()["prefix"]