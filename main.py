import discord
from pickle import dump, load
from discord.ext import commands
TOKEN = 'Enter your bot token here' 

try:
    with open('guildlist','rb') as f:
        guilds = load(f) # Loading guild list from file
except (FileNotFoundError, EOFError): # If file doesn't exist, create it
    guilds = []
    with open('guildlist', 'wb') as f:
        dump(guilds, f) # Saving guild list to file


intents = discord.Intents.all()

bot = commands.Bot(intents=intents) 

bot.load_extension("cogs.moderation")

bot.load_extension("cogs.messagelogging")


@bot.slash_command(
        name="ping",
        description= "Checks if bot is online and answers to commands",
        guild_ids = guilds
)
async def ping(ctx):
    await ctx.respond(f"Pong! {round(bot.latency * 1000)}ms")

@bot.event
async def on_guild_join(guild):
    guilds.append(guild.id) # Adding guild to list of guilds
    with open('guildlist', 'wb') as f:
        dump(guilds, f) # Saving guild list to file

@bot.event
async def on_ready(guilds=guilds):
    guilds = [guild.id for guild in bot.guilds]
    with open('guildlist', 'wb') as f:
        dump(guilds, f) 
    print(f"Logged in as {bot.user}. Running on {len(guilds)} servers")
    



bot.run(TOKEN)
