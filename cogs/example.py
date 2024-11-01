import discord, asyncio, pickle
from discord.ext import commands
bot = commands.Bot()

with open("./guildlist", "rb") as f:
    guilds = pickle.load(f)


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mod = bot.create_group("nothing", "Nothing")

    @mod.command(guild_ids = guilds, description='Makes nothing')
    async def nothing(self):
        return


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Example(bot))