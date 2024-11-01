import discord, pickle,os
import google.generativeai as genai
from discord.ext import commands
bot = commands.Bot()
with open('./apikey', "r", encoding= 'utf-8') as f:
    apikey = f.read()
genai.configure(api_key=apikey)
if not os.path.exists("./historyguilds"):
    with open("./historyguilds", "wb") as f:
        pickle.dump({}, f)
with open("./historyguilds", "rb") as f:
    guildhistory = pickle.load(f)
with open("./guildlist", "rb") as f:
    guilds = pickle.load(f)

safety =  [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    genai = bot.create_group("genai", "Generative ai commands")
  
    @genai.command(guild_ids = guilds, description='Clear context in that channel')
    @commands.has_guild_permissions(manage_channels=True)
    async def clearcontext(self, ctx):
        guildhistory[ctx.guild.id][ctx.channel.id]['history'] = []
        with open("./historyguilds", "wb") as f:
            pickle.dump(guildhistory, f)
        await ctx.respond('Cleared context')
        

    @genai.command(guild_ids = guilds, description='Switches answering without pinging bot in this channel')
    @commands.has_guild_permissions(manage_channels=True)
    async def answerwithoutping(self, ctx):
        try:
            status = guildhistory[ctx.guild.id][ctx.channel.id]['answerwithoutping']
            guildhistory[ctx.guild.id][ctx.channel.id]['answerwithoutping'] = not status
            with open("./historyguilds", "wb") as f:
                    pickle.dump(guildhistory, f)
            await ctx.respond('Answering without pinging bot in this channel is now ' + str(not status))
        except KeyError:
            if ctx.guild.id not in guildhistory:
                guildhistory[ctx.guild.id] = {}
            if ctx.channel.id not in guildhistory[ctx.guild.id]:
                guildhistory[ctx.guild.id][ctx.channel.id] = {'history':[], 'answerwithoutping':True}
            with open("./historyguilds", "wb") as f:
                    pickle.dump(guildhistory, f)
            await ctx.respond('Answering without pinging bot in this channel is now True')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not isinstance(message.channel, discord.DMChannel):
            pass
        else: return
        try:
            
            if not guildhistory[message.guild.id][message.channel.id]['answerwithoutping']:
                pass
            else:
                history = guildhistory[message.guild.id][message.channel.id]['history']
                model=genai.GenerativeModel(model_name="gemini-1.5-flash", safety_settings=safety)
                chat = model.start_chat(history=history)        

                response = chat.send_message((message.content).replace(f"<@{self.bot.user.id}>", ""))

                await message.channel.send(response.text)
                guildhistory[message.guild.id][message.channel.id]['history'] = chat.history
                if not os.path.exists("./historyguilds"):
                    with open("./historyguilds", "wb") as f:
                        pickle.dump(chat.history, f)
                return
        except KeyError:
            pass
        if self.bot.user.mentioned_in(message):
            if message.guild.id not in guildhistory:
                guildhistory[message.guild.id] = {}
            if message.channel.id not in guildhistory[message.guild.id]:
                guildhistory[message.guild.id][message.channel.id] = {'history':[], 'answerwithoutping':False}
            history = guildhistory[message.guild.id][message.channel.id]['history']
            model=genai.GenerativeModel(model_name="gemini-1.5-flash", safety_settings=safety)

            chat = model.start_chat(history=history)        
    
            response = chat.send_message((message.content).replace(f"<@{self.bot.user.id}>", ""))

            await message.channel.send(response.text)
            guildhistory[message.guild.id][message.channel.id]['history'] = chat.history
            if not os.path.exists("./historyguilds"):
                with open("./historyguilds", "wb") as f:
                    pickle.dump(chat.history, f)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Ai(bot))