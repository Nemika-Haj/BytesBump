import random
from discord import Embed, Color

class Embeds:
    def __init__(self, message):
        self.message = message

    def success(self, **kwargs):
        embed = Embed(
            description=self.message,
            color=Color.green()
        )
        for i in kwargs:
            embed.add_field(name=i.replace("_", " "), value=kwargs[i])
        return embed

    def error(self, **kwargs):
        embed = Embed(
            description=self.message,
            color=Color.red()
        )
        for i in kwargs:
            embed.add_field(name=i.replace("_", " "), value=kwargs[i])
        return embed

    def warn(self, **kwargs):
        embed = Embed(
            description=self.message,
            color=Color.orange()
        )
        for i in kwargs:
            embed.add_field(name=i.replace("_", " "), value=kwargs[i])
        return embed