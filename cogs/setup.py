import discord, asyncio

from core.database import Servers
from core.embeds import Embeds
from core.files import Data

commands = discord.ext.commands

class BumpSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Data("config").yaml_read()
        global setting_up 
        setting_up = []
    
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.check(lambda ctx: ctx.guild not in setting_up)
    @commands.command()
    async def setup(self, ctx):
        guild = ctx.guild

        if Servers(guild.id).get():
            return await ctx.send(embed=Embeds(f"This server was already setup! Use `{self.config['prefix']}delete` to initialize another setup!").error())

        embed = discord.Embed(
            title="🔄 Setting Up...",
            color=discord.Color.green()
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url_as(static_format="png"))

        embed.description = "Enter your **Server's Description**! Remember that it must be between **10** and **2048** characters long!"
        await ctx.send(embed=embed)
        try:
            description = (await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content
            if len(description) > 2048:
                return await ctx.send(embed=Embeds("Setup canceled, your description is too long!").error())
            elif len(description) < 10:
                return await ctx.send(embed=Embeds("Setup canceled, your description is too short!").error())
        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup canceled, timeout!").error())

        embed.description = "Enter the channel to fetch invites from. Make sure the bot has permission to **Create Instant Invite** for it!"
        await ctx.send(embed=embed)
        try:
            invite = await commands.TextChannelConverter().convert(ctx, (await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content)
            
            if not invite.permissions_for(ctx.me).create_instant_invite:
                return await ctx.send(embed=Embeds("Setup canceled, I cannot **Create Instant Invites** for it!").error())

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup canceled, timeout!").error())
        except commands.ChannelNotFound:
            return await ctx.send(embed=Embeds("Setup canceled, channel not found!").error())
        
        embed.description = "Enter the channel to send bumps at. Make sure the bot has permission to **Manage Webhooks** for it!"
        await ctx.send(embed=embed)
        try:
            listing = await commands.TextChannelConverter().convert(ctx, (await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content)
            
            if not listing.permissions_for(ctx.me).manage_webhooks:
                return await ctx.send(embed=Embeds("Setup canceled, I cannot **Manage Webhooks** for it!").error())

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup canceled, timeout!").error())
        except commands.ChannelNotFound:
            return await ctx.send(embed=Embeds("Setup canceled, channel not found!").error())
        
        embed.description = "Enter a `HEX` color for your bump embed!"
        await ctx.send(embed=embed)
        try:
            color = int((await self.bot.wait_for(
                'message',
                timeout=120,
                check=lambda message: message.author.id == ctx.author.id and len(message.content) and message.channel.id == ctx.channel.id
            )).content, 16)

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup canceled, timeout!").error())
        except ValueError:
            return await ctx.send(embed=Embeds("Setup canceled, invalid color!").error())

        webhook = await listing.create_webhook(name=self.config['bot_name'], avatar=self.bot.avatar_url)

        Servers(ctx.guild.id).add(webhook=webhook.id, listing=listing, color=color, description=description)

        await ctx.send("Setup complete! Server added to DB and the webhook was created.")

    @setup.before_invoke
    async def add_to_setting_up(self, ctx):
        setting_up.append(ctx.guild)

    @setup.after_invoke
    @setup.error
    async def remove_from_setting_up(self, ctx):
        try:
            setting_up.remove(ctx.guild)
        except: pass

def setup(bot):
    bot.add_cog(BumpSetup(bot))