import discord

from core.database import Servers
from core.files import Data
from core import embeds

commands = discord.ext.commands

def getPrefix(bot, message):
    prefix = [Data('config').yaml_read()['prefix']]
    if message.guild:
        server = Servers(message.guild.id)
        prefix = [server.getPrefix()]
    return commands.when_mentioned_or(*prefix)(bot, message)

class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def setprefix(self, ctx, *, prefix=None):
        server = Servers(ctx.guild.id)
        if not prefix or prefix == "p!":
            if server.hasPrefix: server.deletePrefix
            return await ctx.send(embed=embeds.Embeds(f"The prefix was reset to default! `({Data('config').yaml_read()['prefix']})`").success())
        server.setPrefix(prefix)
        return await ctx.send(embed=embeds.Embeds(f"The prefix was set to `{prefix}`!").success())
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        server = Servers(guild.id)
        if server.hasPrefix: server.deletePrefix

def setup(bot):
    bot.add_cog(SetPrefix(bot))