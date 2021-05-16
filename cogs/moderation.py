import discord
from discord.ext import commands
import json
from cogs.utils.checks import get_user
import asyncio
import sys
import time
from cogs.utils.checks import get_confirmed
from cogs.utils.emoji import tick,cross
from cogs.utils.color import fetch_color
import re
from cogs.utils.lister import lister_str


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600,"s":1,"m":60,"d":86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key,value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)

class Moderation(commands.Cog,name="Moderation Commands"):
    def __init__(self,bot):
        self.bot = bot


    # mod_list = open(f"{sys.path[0]}\\cogs\\modroles.txt","r")
    # content = mod_list.read()
    # print(content)

    @commands.command()
    # @commands.has_any_role(content)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member,*,reason=None):
        ''' Kick a member from this server '''
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry you can't kick someone above you")
        elif ctx.guild.me.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't kick someone above me.")
        elif member == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        elif member == ctx.message.author:
            return await ctx.send(f"{cross} | Do you really want to do it to yourself?")
        else:
            member = get_user(ctx.message,member)
            if member:
                if reason != None:
                    await member.kick(reason=reason)
                    
                    await ctx.send(f"{tick} | {member.mention} has been kicked for {reason}")
                else:
                    await member.kick(reason="You have been kicked out from the server")
                    
                    await ctx.send(f"{tick} | {member.mention} has been kicked")
            else:
                await ctx.send(f"{cross} | Member {member.mention} is not found!")
    

    # @commands.command()
    # @commands.is_owner()
    # async def addmod(self,ctx,*,role):
    #     if role.startswith("@"):
    #         role = role.remove("@")
    #     file = open(f"{sys.path[0]}\\cogs\\modroles.txt","r")
    #     content = file.read()
    #     if not content:
    #         if role:
    #             file = open(f"{sys.path[0]}\\cogs\\modroles.txt","a")
    #             file.write('"'+role+'"')
    #             file.close()
    #             await ctx.send(f"Role @{role} has been added as moderator")
    #         else:
    #             await ctx.send("Please specify a role to add as a moderator")
    #     else:
    #         file = open(f"{sys.path[0]}\\cogs\\modroles.txt","a")
    #         file1 = open(f"{sys.path[0]}\\cogs\\modroles.txt","r")
    #         # content = list(file1.read())
    #         content = [file1.read()]
    #         # print(content)
    #         temp_role = '"'+role+'"'
    #         for roles in content:
    #             if temp_role == '"'+roles+'"':
    #                 await ctx.send(f"Role @{role} is already a mod")
    #                 return
    #         file.write(","+'"'+role+'"')
    #         file.close()
    #         await ctx.send(f"Role @{role} has been added as moderator")

    
    # print(content)

    @commands.command()
    # @commands.has_any_role(content)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,reason=None):
        ''' Ban a member from the server '''
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry you can't ban someone above you")
        elif ctx.guild.me.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't ban someone above me.")
        elif member == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        elif member == ctx.message.author:
            return await ctx.send(f"{cross} | Do you really want to do it to yourself?")
        else:
            if reason != None:
                await member.ban(reason=reason)
                # await ctx.channel.purge(limit=1)
                await ctx.send(f"{tick} | {member.mention} has been banned for {reason}")
            else:
                await member.ban(reason="You have been banned from server!")
                await ctx.send(f"{tick} | {member.mention} has been banned")
    

    @commands.command()
    # @commands.has_any_role(content)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self,ctx,*,member:discord.User):
        ''' Unban a member from the server '''
        # await ctx.channel.purge(limit=1)
        banned_users = await ctx.guild.bans()
        member_name = member.name
        bnd_users_names = []
        for ban_entry in banned_users:
            bnd_users_names.append(ban_entry.user.name)
        user = ban_entry.user
        if member_name in bnd_users_names:
            await ctx.guild.unban(user)
            await ctx.send(f"{tick} | {member_name} is unbanned!")
        else:
            return await ctx.send(f"{cross} | User {member_name} is not in the banned list")

    @commands.command()
    # @commands.has_any_role(content)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount:int):
        ''' Clears/purge messages '''
        await ctx.channel.purge(limit=amount+1)
    

    @commands.command(aliases=['sban'],pass_context=True)
    # @commands.has_any_role(content)
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def softban(self,ctx,member:discord.Member,*,reason=None):
        ''' Bans and unbans the user (only if you have the permission) '''
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry you can't soft ban someone above you")
        elif ctx.guild.me.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't ban someone above me.")
        elif member == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        elif member == ctx.message.author:
            return await ctx.send(f"{cross} | Do you really want to do it to yourself?")
        else:
            if reason != None:
                await member.ban(reason=reason)
                await ctx.guild.unban(member)
                await ctx.send(f"{tick} | Member {member.mention} has been soft banned for reason : {reason}")
            else:
                await member.ban(reason=f"You have been banned and unbanned from server {ctx.guild.name}")
                await ctx.guild.unban(member)
                await ctx.send(f"{tick} | Member {member.mention} has been banned and unbanned")
    

    @commands.command()
    # @commands.has_any_role(content.replace('"','').split(','))
    @commands.bot_has_permissions(mute_members=True)
    @commands.has_permissions(mute_members=True)
    async def mute(self,ctx,user:discord.Member,*,reason=None):
        ''' Chat mutes the user (only if you have perms) '''
        # ==========================================================
        # role = discord.utils.get(user.server.roles,name="Muted!")
        # await ctx.add_roles(user,role)
        # await ctx.send(f"Member {user.name} has been muted!")
        # await user.edit(mute=True)
        # await ctx.send(f"Member {user.name} has been muted!")
        #============================================================
        if ctx.message.author.top_role < user.top_role:
            return await ctx.send(f"{cross} | Sorry you can't mute someone above you")
        elif ctx.guild.me.top_role < user.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't mute someone above me.")
        elif user == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        elif user == ctx.message.author:
            return await ctx.send(f"{cross} | Do you really want to do it to yourself?")
        else:
            role = discord.utils.get(ctx.guild.roles,name="Muted!")
            if not role:
                try:
                    muted = await ctx.guild.create_role(name="Muted!",reason="To be used for muting!")
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted,send_messages=False,read_messages=False,read_message_history=False)

                except discord.Forbidden:
                    return await ctx.send(f"{cross} | I don't have permissions to make a role")
                await user.add_roles(muted)
                if reason == None:
                    await ctx.send(f"{tick} | {user.mention} has been muted")
                else:
                    await ctx.send(f"{tick} | {user.mention} has been muted for reason : {reason}")
            else:
                await user.add_roles(role)
                if reason == None:
                    await ctx.send(f"{tick} | {user.mention} has been muted")
                else:
                    await ctx.send(f"{tick} | {user.mention} has been muted for reason : {reason}")


    @commands.command()
    # @commands.has_any_role(content)
    @commands.bot_has_permissions(mute_members=True)
    @commands.has_permissions(mute_members=True)
    async def unmute(self,ctx,user:discord.Member):
        ''' Unmutes a muted user '''
        role = discord.utils.get(ctx.guild.roles,name="Muted!")
        if role in user.roles:
            await user.remove_roles(discord.utils.get(ctx.guild.roles,name="Muted!"))
            await ctx.send(f"{tick} | {user.mention} has been unmuted!")
        else:
            await ctx.send(f"{cross} | User {user.mention} is already unmuted!")

    
    @commands.command(alias=['tmute','tempmute'])
    # @commands.has_any_role(content)
    @commands.bot_has_permissions(mute_members=True)
    @commands.has_permissions(mute_members=True)
    async def timemute(self,ctx,user:discord.Member,time,*,reason=None):
        ''' Timemute a user '''
        t = convert(time)
        time = t
        if not user:
            return await ctx.send(f"{cross} | Please mention the user to whom you want to time mute.")
        elif ctx.message.author.top_role < user.top_role:
            return await ctx.send(f"{cross} | Sorry you can't time mute to someone above you")
        elif ctx.guild.me.top_role < user.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't mute someone above me.")
        elif user == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        elif user == ctx.message.author:
            return await ctx.send(f"{cross} | Do you really want to do it to yourself?")
        else:
            
            role = discord.utils.get(ctx.guild.roles,name="Muted!")
            if self.bot.user == user:
                await ctx.send(f"{cross} | Bruh! -_- You can't mute me!")
            else:
                await user.add_roles(role,reason=reason)
                if time < 1:
                    await ctx.send(f"{tick} | User {user.mention} has been muted for {time} minutes")
                elif time == 1:
                    await ctx.send(f"{tick} | User {user.mention} has been muted for {time} minute")

            if time == 0 or time < 0:
                await ctx.send(f"{cross} | Please enter a valid time period")

            elif time > 0:
                await asyncio.sleep(time * 60)
                await user.remove_roles(role,reason="Times up! Now enjoy")
                await ctx.send(f"{tick} | User {user.mention} has been unmuted!")

    
    @commands.command()
    # @commands.has_any_role(content)
    @commands.bot_has_permissions(manage_guild=True)
    @commands.has_permissions(manage_guild=True)
    async def warn(self,ctx,user:discord.Member,*,reason):
        ''' Warns a user for a reason '''
        if ctx.message.author.top_role < user.top_role:
            return await ctx.send(f"{cross} | Sorry you can't warn someone above you")
        elif ctx.guild.me.top_role < user.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't warn someone above me.")
        elif user == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        elif user == ctx.message.author:
            return await ctx.send(f"{cross} | Do you really want to do it to yourself?")
        else:
            await ctx.send(f"{tick} | User {user.mention} has been warned for {reason}")
            await user.send(f"You have been warned for {reason} in {ctx.guild.name}")


    @commands.command()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self,ctx,channel:discord.TextChannel=None):
        ''' Locks a channel. '''
        channel = channel or ctx.channel
        try:
            if ctx.guild.default_role not in channel.overwrites:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                await ctx.send(f"🔒 Channel {channel} locked down. Only roles with permissions given can speak.")
                await channel.edit(overwrites=overwrites)
            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = False
                await ctx.send(f"🔒 Channel {channel} locked down. Only roles with permissions given can speak.")
                await channel.set_permissions(ctx.guild.default_role,overwrite=overwrites)
        except discord.Forbidden:
            await ctx.send(f"{cross} | Bot is missing permissions.")
        

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self,ctx,channel:discord.TextChannel=None):
        ''' Unlocks a locked channel '''
        channel = channel or ctx.channel
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"🔓 Channel {channel} has been removed from locked down.")
        except discord.Forbidden:
            await ctx.send(f"{cross} | Bot is missing permissions.")


    @commands.command(aliases=["lbans"])
    # @commands.bot_has_permissions(kick_members=True)
    # @commands.has_permissions(kick_members=True)
    async def listbans(self,ctx): # GONNA GET CHANGED TO DB
        ''' List the bans in the server '''
        bans = await ctx.guild.bans()
        await lister_str(ctx=ctx,your_list=[b.user.name for b in bans],color=await fetch_color(bot=self.bot,ctx=ctx),title=f"List of bans in {ctx.guild.name}")
        

    @commands.command(aliases=["cnick"])
    # @commands.bot_has_permissions(kick_members=True)
    # @commands.has_permissions(kick_members=True)
    async def changenick(self,ctx,member:discord.Member,*,name):
        ''' Change the nickname of any member '''
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry you can't change the nickname of someone above you")
        elif ctx.guild.me.top_role < member.top_role:
            return await ctx.send(f"{cross} | Sorry, I can't change nickname of someone above me.")
        elif member == ctx.guild.owner:
            return await ctx.send(f"{cross} | You can't use this command on owner")
        else:
            await member.edit(nick=name)
            await ctx.send(f"{tick} | {member} nickname changed to {name} by {ctx.message.author}")

    
    # To be called in other commands!
    # @commands.command(hidden=True)
    # async def loading(self,ctx):
    #     message = await ctx.send("Loading... \ ")
    #     while True:
    #         await message.edit(content="Loading... / ")
    #         asyncio.sleep(0.5)
    #         await message.edit(content="Loading... \ ")

            # ✅
    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def addemoji(self,ctx):
    #     image_path1 = f"{sys.path[0]}//emojis//tickmark.png"
    #     await ctx.guild.create_custom_emoji(name=('tickmark'),image=(image_path1))


def setup(bot):
    try:
        bot.add_cog(Moderation(bot))
        print(OKGREEN+"[STATUS OK] Moderation cog is ready!")
    except:
        print(FAIL+"[CRITICAL] Cant load moderation cog!")
