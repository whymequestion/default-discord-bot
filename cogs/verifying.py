import discord, asyncio, pickle
from discord.ext import commands
bot = commands.Bot()

with open("./guildlist", "rb") as f:
    guilds = pickle.load(f)

class VerificationView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.ctx = ctx
        self.message = None
        self.role = None
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author
    
    async def start(self, role: discord.Role):
        self.message = await self.ctx.send(content='Click the button below to verify yourself', view=self)
        self.role = role
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def verify(self, button: discord.Button, interaction: discord.Interaction):
        member = interaction.user
        role = self.role
        await member.add_roles(role)
        await interaction.response.send_message(content=f'You have been verified!', view=None, ephemeral=True)


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mod = bot.create_group("verification", "Verification")

    @mod.command(guild_ids = guilds, description='Creates a button for verification')
    @commands.has_guild_permissions(administrator=True)
    async def create(self, ctx, role: discord.Role):
        view = VerificationView(ctx)
        await view.start(role=role)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Verification(bot))