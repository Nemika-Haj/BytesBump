from .files import Data
from discord.ext import commands

config = Data("config").yaml_read()

def manager():
    def predicate(ctx):
        return ctx.author.id in config["managers"]
    return commands.check(predicate)