import discord, pickle
from discord.ext import commands
bot = commands.Bot()
logchannel = {}

# Load guild data from file
with open("./guildlist", "rb") as f:
    guilds = pickle.load(f)
class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._logchannel = None


    @commands.slash_command(name="setlogchannel", description= "Set the log channel")
    @commands.has_guild_permissions(manage_channels=True)
    async def set_log_channel(self, ctx, channel: discord.TextChannel):
        global logchannel
        logchannel[ctx.guild.id] = channel.id
        try:
            with open('./logchannels','rb') as f:
                logchannel = pickle.load(f) # Loading channel list from file
        except (FileNotFoundError, EOFError): # If file doesn't exist, create it
            with open('./logchannels', 'wb') as f:
                pickle.dump(logchannel, f) # Saving channel list to file
        await ctx.respond(f"Log channel has been set to {channel.mention}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.user.bot: return
        try:
            with open('./logchannels', 'rb') as f:
                logchannel = pickle.load(f)[message.guild.id]
        except Exception:
            return
        log_channel = self.bot.get_channel(logchannel)
        if log_channel is None:
            return

        embed = discord.Embed(title="Message Deleted", colour=0xff0000)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Author", value=message.author.mention, inline=False)
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"Message ID: {message.id}")

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.user.bot: return
        try:
            with open('./logchannels', 'rb') as f:
                logchannel = pickle.load(f)[before.guild.id]
        except Exception:
            return
        log_channel = self.bot.get_channel(logchannel)
        if log_channel is None:
            return
        embed = discord.Embed(title="Message Edited", colour=0x00ff00)
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"Message ID: {before.id}")

        await log_channel.send(embed=embed)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Logging(bot))

