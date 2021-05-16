import discord
from discord.ext import commands
import json
import sys
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

class Create(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def channel(self,ctx):
        ''' 
        This command is used to create text channel and voice channels. 
        [s]channel <subcommand> <type> <name> - To create a text channel
        '''

        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    
    # ============== SOME CHANGES ARE REQUIRED -_- ==============
    # @channel.command(pass_context=True)
    # @commands.has_permissions(manage_channels=True)
    # @commands.bot_has_permissions(manage_channels=True)
    # async def text(self,ctx,command:str,*,name:discord.TextChannel):
    #     if command.lower() == "create":
    #         guild = ctx.guild
    #         await guild.create_text_channel(name,overwrites=None,reason=None)
    #         await ctx.send(f"Text channel #{name} has been created!")
    #     elif command.lower() == "delete":
    #         guild = ctx.message.guild
    #         # await guild.delete_channel(discord.TextChannel.name)
    #         await name.delete()
    #         await ctx.send(f"Text channel **{name}** has been deleted!")
    #     elif command.lower() == "clone":
    #         name = str(name)
    #         # print(name)
    #         existing_channel = discord.utils.get(ctx.guild.text_channels,name=name)
    #         if existing_channel is not None:
    #             await existing_channel.clone(reason="I think the channel got nuked or another channel is needed!")
    #             await ctx.send(f"Channel **{name}** is cloned!")
    #         else:
    #             await ctx.send(f"No channel named **{name}** was found in the server!")
    
    # @commands.command()
    # @commands.bot_has_permissions(manage_channels=True)
    # @commands.has_permissions(manage_channels=True)
    # async def rename(self,ctx,name,*,new_name):
    #         # name = str(name)
    #     '''
    #     Renames a channel. Make sure to give channel name.
    #     '''
    #     channel_text = discord.utils.get(ctx.guild.text_channels,name=name)
    #     channel_voice  = discord.utils.get(ctx.guild.voice_channels,name=name)
    #     if channel_text is not None and channel_voice is None:
    #         await channel_text.edit(name=new_name)
    #         await ctx.send(f"Text channel **{name}** renamed to **{new_name}**")
    #     elif channel_text is None and channel_voice is not None:
    #         await channel_voice.edit(name=new_name)
    #         await ctx.send(f"Voice channel **{name}** renamed to **{new_name}**")
    #     else:
    #         await ctx.send(f"No channel named **{name}** found!")

    #===============================================================================#

    @channel.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def create(self,ctx,type,*,name):
        ''' Create text/voice channel with this command '''
        if type.lower() == "text":
            guild = ctx.guild
            await guild.create_text_channel(name,overwrites=None,reason=None)
            await ctx.send(f"{tick} | Text channel #{name} has been created!")
        elif type.lower() == "voice":
            guild = ctx.guild
            await guild.create_voice_channel(name,overwrites=None,reason=None)
            await ctx.send(f"{tick} | Voice channel **{name}** has been created!") #<:check:773959361953267742> 
        else:
            await ctx.send(f"❌ Please enter a valid type.")



    @channel.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def delete(self,ctx,channel=None):
        ''' Delete any channel with this command '''
        guild = ctx.guild
        channel = discord.utils.get(ctx.guild.channels,name=channel)
        await channel.delete()
        await ctx.send(f"{tick} | Channel **{channel}** deleted!")

    

    @channel.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def rename(self,ctx,channel_name,*,new_name):
        ''' Rename any channel with this command '''
        channel_text = discord.utils.get(ctx.guild.text_channels,name=channel_name)
        channel_voice  = discord.utils.get(ctx.guild.voice_channels,name=channel_name)
        if channel_text is not None and channel_voice is None:
            await channel_text.edit(name=new_name)
            await ctx.send(f"{tick} | Text channel **{channel_name}** renamed to **{new_name}**")
        elif channel_text is None and channel_voice is not None:
            await channel_voice.edit(name=new_name)
            await ctx.send(f"{tick} | Voice channel **{channel_name}** renamed to **{new_name}**")
        else:
            await ctx.send(f"{cross} | No channel named **{channel_name}** found!")

    

    @channel.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def clone(self,ctx,*,channel_name):
        ''' Clone any channel with this command '''
        channel_name = str(channel_name)
        # print(name)
        existing_channel = discord.utils.get(ctx.guild.channels,name=channel_name)
        if existing_channel is not None:
            await existing_channel.clone(reason="I think the channel got nuked or another channel is needed!")
            await ctx.send(f"{tick} | Channel **{channel_name}** is cloned!")
        else:
            await ctx.send(f"{cross} | No channel named **{channel_name}** was found in the server!")

    


    @channel.command(pass_context=True)
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
            await ctx.send(f"{cross} |  Bot is missing permissions.")
        
    
            

    @channel.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self,ctx,channel:discord.TextChannel=None):
        '''
        Unlock a locked channel.
        '''
        channel = channel or ctx.channel
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"🔓 Channel {channel} has been removed from locked down.")
        except discord.Forbidden:
            await ctx.send(f"{cross} |  Bot is missing permissions.")

    
    

    @channel.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self,ctx,channel=None,*,time:int):
        ''' Enable slowmode to any channel '''
        if time !=0 and time > 0:
            channel = discord.utils.get(ctx.guild.channels,name=channel)
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send(f"{tick} | Slowmode enabled for channel **{channel}**")
        else:
            await ctx.send(f"{cross} | Please enter a valid time")


    @channel.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def hide(self,ctx,*,channel_name=None):
        ''' Hide any channel with this command '''
        # guild = ctx.guild
        # print(ctx.channel) # GIVES THE CURRENT CHANNEL 
        channel = discord.utils.get(ctx.guild.channels,name=channel_name)
        if channel is not None:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
        elif channel is None:
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if channel is not None and channel in ctx.guild.text_channels and overwrite.view_channel == False:
            await ctx.send(f"{cross} | Channel **{channel}** is already hidden")
        elif channel is not None and channel in ctx.guild.voice_channels and overwrite.connect == False:
            await ctx.send(f"{cross} | Channel **{channel}** is already hidden")
        elif channel is None and channel in ctx.guild.text_channels and overwrite.view_channel == False:
            await ctx.send(f"{cross} | Channel **{channel}** is already hidden")
        elif channel is None and channel in ctx.guild.voice_channels and overwrite.connect == False:
            await ctx.send(f"{cross} | Channel **{channel}** is already hidden")
        elif channel is not None and channel in ctx.guild.text_channels:
            # overwrite = {
            #     ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
            # }
            # await channel.edit(overwrite=overwrite)
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
            await ctx.send(f"{tick} | Channel **{channel}** is now hidden!")
        elif channel is not None and channel in ctx.guild.voice_channels:
            await channel.set_permissions(ctx.guild.default_role, connect=False)
            await ctx.send(f"{tick} | Channel **{channel}** is now hidden!")
        elif channel is not None and channel not in ctx.guild.text_channels:
            await ctx.send(f"{cross} | No channel named **{channel}** found!")
        elif channel is not None and channel not in ctx.guild.voice_channels:
            await ctx.send(f"{cross} | No channel named **{channel}** found!")
        elif channel is None and ctx.channel in ctx.guild.text_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
            await ctx.send(f"{tick} | Channel **{ctx.channel}** is now hidden!")
        elif channel is None and ctx.channel in ctx.guild.voice_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, connect=False)
            await ctx.send(f"{tick} | Channel **{ctx.channel}** is now hidden!")
        else:
            pass
    
    
    @channel.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unhide(self,ctx,*,channel_name=None):
        ''' Unhide a hidden channel with this command '''
        guild = ctx.guild
        channel = discord.utils.get(ctx.guild.channels,name=channel_name)
        if channel is not None:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
        elif channel is None:
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if channel is not None and channel in ctx.guild.text_channels and overwrite.view_channel == True:
            await ctx.send(f"{cross} | Channel **{channel}** is already unhidden")
        elif channel is not None and channel in ctx.guild.voice_channels and overwrite.connect == True:
            await ctx.send(f"{cross} | Channel **{channel}** is already unhidden")
        elif channel is None and channel in ctx.guild.text_channels and overwrite.view_channel == True:
            await ctx.send(f"{cross} | Channel **{channel}** is already unhidden")
        elif channel is None and channel in ctx.guild.voice_channels and overwrite.connect == True:
            await ctx.send(f"{cross} | Channel **{channel}** is already unhidden")
        elif channel is not None and channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role,view_channel=True)
            await ctx.send(f"{tick} | Channel **{channel}** is now unhidden!")
        elif channel is not None and channel in ctx.guild.voice_channels:
            await channel.set_permissions(ctx.guild.default_role,connect=True)
            await ctx.send(f"{tick} | Channel **{channel}** is now unhidden!")
        elif channel is None and ctx.channel in ctx.guild.text_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
            await ctx.send(f"{tick} | Channel **{ctx.channel}** is now unhidden!")
        elif channel is None and ctx.channel in ctx.guild.voice_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, connect=True)
            await ctx.send(f"{tick} | Channel **{ctx.channel}** is now unhidden!")
        else:
            pass



def setup(bot):
    bot.add_cog(Create(bot))
    print(OKGREEN + "[STATUS OK] Create cog is ready!")