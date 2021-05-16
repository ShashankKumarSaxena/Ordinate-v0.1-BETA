import discord
from discord.ext import commands
from colorama import init,Fore
from cogs.utils.emoji import tick

init(autoreset=True)

class Status(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(pass_context=True)
    @commands.is_owner()
    async def status(self,ctx):
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    @status.command()
    async def listening(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")

    @status.command()
    async def playing(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")


    @status.command()
    async def streaming(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")


    @status.command()
    async def watching(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")

    
    @status.command()
    async def competing(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing,name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")

    @status.command()
    async def custom(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")

    @status.command()
    async def game(self,ctx,status:str=None,*,text):
        text = discord.utils.escape_markdown(str(text),as_needed=False,ignore_links=True)
        text = text.replace("\\","")
        st = ""
        if status == None:
            st = discord.Status.online
        elif status == "online":
            st = discord.Status.online
        elif status == "offline":
            st = discord.Status.offline
        elif status == "idle":
            st = discord.Status.idle
        elif status == "dnd":
            st = discord.Status.dnd
        await self.bot.change_presence(activity=discord.Game(name=text),status=st)
        await ctx.send(f"{tick} | Status has been changed to `{text}`")



def setup(bot):
    bot.add_cog(Status(bot))
    print(Fore.GREEN + "[STATUS OK] Status cog is ready!")