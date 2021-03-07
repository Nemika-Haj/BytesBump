import discord
from core import embeds

commands = discord.ext.commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=embeds.Embeds(f"Missing `{error.param}` as a required argument.").error())
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=embeds.Embeds("You are not allowed to do this.").error())
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            return await ctx.send(embed=embeds.Embeds(f"**You are on cooldown!** You can use this command again in **{seconds} seconds**.").error())
        else:
            await ctx.send(embed=embeds.Embeds("There was an error executing this command.").error(Error=error))
            raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))