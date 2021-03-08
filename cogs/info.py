import discord

from core.database import Servers
from core.files import Data
from core.embeds import Embeds

commands = discord.ext.commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Data("config").yaml_read()

    @commands.guild_only()
    @commands.command(aliases=['about'])
    async def info(self, ctx):
        return await ctx.send(embed=discord.Embed(
            title=f"{self.config['bot_name']} | Information",
            color=discord.Color.blurple()
        )
        .add_field(name="Version", value=self.config['version'])
        .add_field(name="Library", value=f"Discord.py v{discord.__version__}")
        .add_field(name="Latency", value=f"{round(self.bot.latency*1000)}ms")
        .add_field(name="Servers", value=len(self.bot.guilds))
        .add_field(name="Active Servers", value=len([i for i in Servers().get_all()]))
        .add_field(name="Open Source", value="[View](https://github.com/Nemika-Haj/BytesBump)") # DO NOT REMOVE
        .set_footer(text="Made by • " + ', '.join([str((await self.bot.fetch_user(i))) for i in self.config['managers']])))

    @commands.guild_only()
    @commands.command(aliases=['support'])
    async def help(self, ctx):
        return await ctx.send(embed=discord.Embed(
            title=f"{self.config['bot_name']} | Help",
            description=Data("help").read(),
            color=discord.Color.blurple()
        ))

    @commands.guild_only()
    @commands.command(aliases=["add"])
    async def invite(self, ctx):
        return await ctx.send(embed=Embeds(f"[Click here to invite me!](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=537152577&scope=bot)"))

def setup(bot):
    bot.add_cog(Info(bot))