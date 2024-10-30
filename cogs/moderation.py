import discord, asyncio, pickle
from discord.ext import commands
bot = commands.Bot()

with open("./guildlist", "rb") as f:
    guilds = pickle.load(f)
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def cog_before_invoke(self, ctx):
        if not ctx.guild:
            return await ctx.respond("This command can only be used in a server.")

        if not ctx.author.guild_permissions.ban_members:
            return await ctx.respond("You need the 'Ban Members' permission to use this command.")

        if not ctx.author.guild_permissions.mute_members:
            return await ctx.respond("You need the 'Mute Members' permission to use this command.")

        if not ctx.author.guild_permissions.kick_members:
            return await ctx.respond("You need the 'Kick Members' permission to use this command.")

        if not ctx.guild.me.guild_permissions.ban_members:
            return await ctx.respond("I need the 'Ban Members' permission to use this command.")
        # Repeat the same checks for the other permissions you need.


    mod = bot.create_group("mod", "Moderation")

    @mod.command(guild_ids = guilds, description='This is the ban command')
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        await member.ban(reason=reason)
        await ctx.respond(f"User {member.mention} has been banned.")

    @mod.command(guild_ids = guilds, description='This is the mute command')
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, time: int):
        if member.bot:
            await ctx.respond("Cannot mute a bot.")
            return
        guild = ctx.guild
        m = discord.utils.get(guild.members, id=member.id)
        role = discord.utils.get(guild.roles, name="Muted")
        
        if role is None:
            role = await guild.create_role(name="Muted", reason="role for muting members")
            role_permissions = discord.Permissions(send_messages=False, read_messages=True, read_message_history=True)
            await role.edit(permissions=role_permissions)
            for channel in guild.channels:
                await channel.set_permissions(role, send_messages=False)

                
        await m.add_roles(role)
        await ctx.defer()
        await ctx.respond(f"User {member.mention} has been muted for {time} seconds")
        await asyncio.sleep(time)
        await m.remove_roles(role)
        
    @mod.command(guild_ids = guilds, description='This is the kick command')
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        await member.kick(reason=reason)
        await ctx.respond(f"User {member.mention} has been kicked.")
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Moderation(bot))