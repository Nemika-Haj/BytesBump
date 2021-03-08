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
            )).content.replace("#", ""), 16)

        except asyncio.TimeoutError:
            return await ctx.send(embed=Embeds("Setup canceled, timeout!").error())
        except ValueError:
            return await ctx.send(embed=Embeds("Setup canceled, invalid color!").error())

        webhook = await listing.create_webhook(name=self.config['bot_name'])

        Servers(ctx.guild.id).add(webhook=webhook.id, invite=invite.id, color=color, description=description)

        await ctx.send("Setup complete! Server added to DB and the webhook was created.")

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.check(lambda ctx: ctx.guild not in setting_up)
    @commands.command()
    async def delete(self, ctx):
        if not Servers(ctx.guild.id).get():
            return await ctx.send(embed=Embeds("The server does not have any data in the Database!").error())

        confirmation_message = await ctx.send(embed=discord.Embed(
            title="⚠️ Confirmation Required ⚠️",
            description=f"**{ctx.author}**, you're about to delete your server from the database! This will remove all data. **Are you sure?**",
            color=discord.Color.orange()
        ))

        emojis = ["✅", "❎"]

        for emoji in emojis: await confirmation_message.add_reaction(emoji)

        try:
            reaction, user = await self.bot.wait_for(
                'reaction_add',
                timeout=120,
                check=lambda r, u: r.emoji in emojis and r.message.id == confirmation_message.id and u.id == ctx.author.id
            )
        except asyncio.TimeoutError:
            await ctx.send(embed=Embeds("Server deletion canceled due to timeout!").error())
            return await confirmation_message.delete()
        
        if reaction.emoji == emojis[1]:
            return await ctx.send(embed=Embeds("Server deletion canceled.").error())
        
        db_entry = Servers(ctx.guild.id)

        cache_data = db_entry.get()

        db_entry.delete()

        setting_up.remove(ctx.guild)

        del_message = await ctx.send(embed=discord.Embed(
            title="🗑️ Server Deleted",
            description="The server was deleted from the database! You also can react below within one minute to restore it.",
            color=discord.Color.green()
        ))

        await del_message.add_reaction("♻️")

        try:
            await self.bot.wait_for(
                'reaction_add',
                timeout=60,
                check=lambda r,u: r.emoji == "♻️" and r.message.id == del_message.id and u.id == ctx.author.id
            )
        except asyncio.TimeoutError:
            try:
                wh = await self.bot.fetch_webhook(cache_data['webhook'])
                await wh.delete()
            except:
                pass
            return await del_message.remove_reaction("♻️", self.bot.user)

        if Servers(ctx.guild.id).get():
            try:
                wh = await self.bot.fetch_webhook(cache_data['webhook'])
                await wh.delete()
            except:
                pass
            return await ctx.send(embed=discord.Embed(
                title="❎ Restore Failed",
                description="The server seems to have been setup from the beginning, therefore restore is not possible.",
                color=discord.Color.red()
            ))

        Servers(ctx.guild.id).add(**cache_data)

        return await ctx.send(embed=discord.Embed(
            title="♻️ Server Restored",
            description="Your server was restored, all data are safe and sound.",
            color=discord.Color.green()
        ))

    @setup.before_invoke
    @delete.before_invoke
    async def add_to_setting_up(self, ctx):
        setting_up.append(ctx.guild)

    @setup.after_invoke
    @delete.after_invoke
    async def remove_from_setting_up(self, ctx):
        try:
            setting_up.remove(ctx.guild)
        except: pass

def setup(bot):
    bot.add_cog(BumpSetup(bot))