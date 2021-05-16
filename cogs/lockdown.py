import discord
from discord.ext import commands
from cogs.utils.checks import load_moderation
import sys
import json
from cogs.utils.color import fetch_color
from cogs.utils.emoji import tick,cross

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Lockdown(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.states = {}

    # @commands.has_permissions(manage_channels=True)
    # @commands.command(pass_context=True,name="lockdown")
    # async def lockdown(self,ctx):
    #     ''' Locks message sending in the channel '''
    #     try:
    #         try:
    #             mod_strings = load_moderation()
    #             mod_role_strings = mod_strings[ctx.message.guild.name]
    #             mod_roles = []
    #             for m in mod_role_strings:
    #                 mod_roles.append(discord.utils.get(ctx.message.guild,name=m))
    #         except:
    #             mod_roles = []
    #         server = ctx.message.guild
    #         overwrites_everyone = ctx.message.channel.overwrites_for(server.default_role)
    #         overwrites_owner = ctx.message.channel.overwrites_for(server.role_hierarchy[0])
    #         if ctx.message.channel.id in self.states:
    #             await ctx.send("🔒 Channel is already locked down. Use 'unlock' to unlock.")
    #             return
    #         states = []
    #         for a in ctx.message.guild.role_hierarchy:
    #             states.append([a,ctx.message.channel.overwrites_for(a).send_messages])
    #         self.states[ctx.message.channel.id] = states
    #         overwrites_owner.send_messages = True
    #         overwrites_everyone.send_messages = False
    #         await ctx.message.channel.set_permissions(server.default_role,overwrite=overwrites_everyone)
    #         for modrole in mod_roles:
    #             await ctx.message.channel.set_permissions(modrole,overwrite=overwrites_owner)
    #         await ctx.send("🔒 Channel locked down. Only roles with permissions given can speak.")
    #     except discord.errors.Forbidden:
    #         await ctx.send("❌ Bot is missing permissions.")


    @commands.command()
    # @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockdown(self,ctx,*,channel=None):
        ''' Lockdown the whole server '''
        channel = channel or ctx.channel
        try:
            if ctx.guild.default_role not in channel.overwrites:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                voice_overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
                }
                for channel in ctx.guild.text_channels:
                    await ctx.send(f"🔒 Channel {channel} locked down. Only roles with permissions given can speak.")
                    await channel.edit(overwrites=overwrites)
                # for channel in ctx.guild.voice_channels:
                #     await ctx.send(f"🔒 Channel {channel} locked down. Only roles with permissions given can speak.")
                #     await channel.set_permissions(ctx.guild.default_role,overwrite=voice_overwrites)
            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                for channel in ctx.guild.text_channels:
                    overwrites = channel.overwrites[ctx.guild.default_role]
                    overwrites.send_messages = False
                    await ctx.send(f"🔒 Channel {channel} locked down. Only roles with permissions given can speak.")
                    await channel.set_permissions(ctx.guild.default_role,overwrite=overwrites)
                # for channel in ctx.guild.voice_channels:
                #     voice_overwrites = channel.overwrites[ctx.guild.default_role]
                #     voice_overwrites.connect = False
                #     await ctx.send(f"🔒 Channel {channel} locked down. Only roles with permissions given can speak.")
                #     await channel.set_permissions(ctx.guild.default_role,overwrite=voice_overwrites)
            else:
                for channel in ctx.guild.text_channels:
                    overwrites = channel.overwrites[ctx.guild.default_role]
                    overwrites.send_messages = True
                    await channel.set_permissions(ctx.guild.default_role,overwrite=overwrites)
                    await ctx.send(f"🔓 Channel {channel} has been removed from locked down.")
                # for channel in ctx.guild.voice_channels:
                #     voice_overwrites = channel.overwrites[ctx.guild.default_role]
                #     voice_overwrites.connect = True
                #     await ctx.send(f"🔓 Channel {channel} has been removed from locked down.")
                #     await channel.set_permissions(ctx.guild.default_role,overwrite=voice_overwrites)

        except discord.Forbidden:
            await ctx.send(f"{cross} |  Bot is missing permissions.")


    
    # @commands.command()
    # @commands.is_owner()
    # @commands.group(pass_context=True)
    # async def mod(self,ctx):
    #     ''' 
    #     Manage the list of moderator roles in you server. [s]help mod for more info.
    #     [s]mod - List your moderator roles that you have set.
    #     [s]mod add <server> <role> - Add a role to the list of moderators on a server.
    #     [s]mod remove <server> <role> - Remove a role from the list of moderators on a server.
    #     '''
    #     if ctx.invoked_subcommand is None:
    #         await ctx.message.delete()
    #         mods = load_moderation()
    #         embed = discord.Embed(title="Moderator Roles",description="")
    #         mod_role_strings = mods[ctx.message.guild.name]
    #         mod_roles = []
    #         for m in mod_role_strings:
    #             mod_roles.append(discord.utils.get(ctx.message.guild.roles,name=m))
            
    #         server = ctx.message.guild.name
    #         embed.description += server + ":\n"
    #         for mod in mod_roles:
    #             embed.description += f"   {mod}\n"
    #         await ctx.send("",embed=embed)


    # # @commands.command()
    # @commands.is_owner()
    # @mod.command(pass_context=True)
    # async def add(self,ctx,server,role):
    #     ''' Add a role to the list of moderators on a server '''
    #     mods = load_moderation()
    #     valid_server = False
    #     valid_role = False
    #     for e in self.bot.guilds:
    #         if e.name == server:
    #             valid_server = True
    #         for f in e.roles:
    #             if f.name == role:
    #                 valid_role = True
    #     if valid_server:
    #         if valid_role:
    #             try:
    #                 mods[server]
    #             except KeyError:
    #                 mods[server] = [role]
    #             else:
    #                 mods[server].append(role)
    #             with open(f"{sys.path[0]}\\cogs\\moderation.json","w+") as f:
    #                 json.dump(mods, f)
    #             await ctx.send(f"Successfully added {role} to the list of mod roles on {server}!")
    #         else:
    #             await ctx.send(f"{role} isn't a role on {server}!")
    #     else:
    #             await ctx.send(f"{server} isn't a server!")
    
    # @mod.command(pass_context=True)
    # # @commands.command()
    # @commands.is_owner()
    # async def remove(self,ctx,server,role):
    #     ''' Removes a role from the list of moderators '''
    #     mods = load_moderation()
    #     try:
    #         mods[server].remove(role)
    #         with open(f"{sys.path[0]}\\cogs\\moderation.json","w+") as f:
    #             json.dump(mods, f)
    #         await ctx.send(f"Successfully removed {role} from the list of mod roles on {server}!")

    #     except(ValueError,KeyError):
    #         await ctx.send("You can't remove something that doesn't exist!")
    



def setup(bot):
    bot.add_cog(Lockdown(bot))
    print(OKGREEN + "[STATUS OK] Lockdown cog is ready!")

