import discord
from discord.ext import commands
import asyncio
from cogs.utils.emoji import cross,tick
from cogs.utils.color import fetch_color
import config

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Message(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def hi(self,ctx):
        await ctx.send("Hello")
    

    # print(colors.items())
    @commands.command(aliases=["lcolors"])
    @commands.bot_has_permissions(send_messages=True)
    async def colors(self,ctx):
        ''' Get color list which you can use to set embed colors too. '''
        colors = {
        "WHITE": "0xFFFFFF",
        "AQUA": "0x1ABC9C",
        "GREEN": "0x2ECC71",
        "BLUE": "0x3498DB",
        "PURPLE": "0x9B59B6",
        "LUMINOUS_VIVID_PINK": "0xE91E63",
        "GOLD": "0xF1C40F",
        "ORANGE": "0xE67E22",
        "RED": "0xE74C3C",
        "NAVY": "0x34495E",
        "DARK_AQUA": "0x11806A",
        "DARK_GREEN": "0x1F8B4C",
        "DARK_BLUE": "0x206694",
        "DARK_PURPLE": "0x71368A",
        "DARK_VIVID_PINK": "0xAD1457",
        "DARK_GOLD": "0xC27C0E",
        "DARK_ORANGE": "0xA84300",
        "DARK_RED": "0x992D22",
        "DARK_NAVY": "0x2C3E50",
        } 
        em = discord.Embed(description="__Color List__",color=await fetch_color(bot=self.bot,ctx=ctx))
        # em.add_field(name=f"{tick} Here are all the list of colors available!",value=f"\n".join(f"Color name : {k} | Value : {v}" for k,v in colors.items()))
        em.add_field(name=f"Here are all the list of colors available!\nUse these color value to change color of role and embeds!",value=f"\n".join(f"Color name : {k} | Value : {v}" for k,v in colors.items()))
        em.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=em)
        # for k,v in colors.items():
            #await ctx.send(f"Color: {k} Value: {v}") # Change to embed to protect bot


    # @commands.command()
    # @commands.has_permissions(manage_messages=True)
    # async def embed(self,ctx,title,color,fields,fieldtitle,fieldvalue,footer,*,msg):
    #     # print(title)
    #     # print(color)
    #     # print(fields)
    #     # print(fieldtitle)
    #     # print(fieldvalue)
    #     # print(footer)
    #     # print(msg)
    #     embed = discord.Embed(
    #         title=title,
    #         description=msg,
    #         color=int(color)
    #     )
    #     embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    #     count = 0
    #     for field in fields:
    #         if count % 3 != 0:
    #             embed.add_field(name=fieldtitle,value=fieldvalue,inline=False)
    #         else:
    #             embed.add_field(name=fieldtitle,value=fieldvalue,inline=True)
    #         count +=1
    #     embed.set_footer(text=footer)
    #     embed.set_image(url=ctx.guild.icon_url)
    #     embed.set_thumbnail(url=ctx.guild.icon_url)
    #     await ctx.send(embed=embed)

    @commands.command()
    # @commands.has_any_role("MOD","SERVER GOD","King Developer")
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def embed(self,ctx,*,msg):
        ''' Send a message as an embed '''
        embed = discord.Embed(
            description = msg,
            color=await fetch_color(bot=self.bot,ctx=ctx)
        )
        await ctx.send(embed=embed)

    @commands.command()
    # @commands.has_any_role("MOD","SERVER GOD","King Developer")
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def dm(self,ctx,user:discord.Member,*,args):
        ''' DM a user '''
        if args != None:
            try:
                await user.send(args)
                await ctx.send(f"{tick} | DM sent to {user.name}")
            except:
                await ctx.send(f"{cross} | User has its DM closed")
        else:
            await ctx.send(f"{cross} | Please specify a message to send")
    
    @commands.command()
    # @commands.has_any_role("MOD","SERVER GOD","King Developer")
    # @commands.has_permissions(send_messages=True)
    # @commands.bot_has_permissions(send_messages=True)
    @commands.is_owner()
    async def dmall(self,ctx,*,args):
        ''' DM all users in server '''
        if args != None:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send(args)
                    await ctx.send(f"{tick} | DM sent to {member.name}")
                except:
                    await ctx.send(f"{cross} | User {member.name} has DM closed")
        else:
            await ctx.send(f"{cross} | Please specify the message to send")

    @commands.command(aliases=["binvite"])
    @commands.bot_has_permissions(send_messages=True)
    async def botinvite(self,ctx):
        ''' Get bot's invite link '''
        em = discord.Embed(description=" ",color=await fetch_color(bot=self.bot,ctx=ctx))
        em.add_field(name="Invite Link - ",value=f"[Click Here!](https://discord.com/api/oauth2/authorize?client_id=798557068998738000&permissions=8&scope=bot)")
        em.set_footer(text=f"Requested by - {ctx.message.author.name}")
        await ctx.send(embed=em)

    @commands.command(aliases=["server"])
    @commands.bot_has_permissions(send_messages=True)
    async def supportserver(self,ctx):
        ''' Get bot's support server link '''
        em = discord.Embed(description=" ",color=await fetch_color(bot=self.bot,ctx=ctx))
        em.add_field(name="Support server link - ",value=f"[Click Here!](https://discord.gg/jkb6dZ5GxZ)")
        em.set_footer(text=f"Requested by - {ctx.message.author.name}")
        await ctx.send(embed=em)

    # @commands.command(aliases=["dinfo"])
    # @commands.bot_has_permissions(send_messages=True)
    # async developerinfo(send_messages=True)
    #     pass

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def timer(self,ctx,seconds):
        # TODO - This command is to be removed in future as it is considered as spamming
        try:
            secondint = int(seconds)
            if secondint > 300:
                await ctx.send(f"{cross} I don't think I can go over 5 minutes")
                raise BaseException
            if secondint <=0:
                await ctx.send(f"{cross} Really nigga? Negative timer!")
                raise BaseException
            
            message = await ctx.send(f"Timer: {seconds}")
            while True:
                secondint -= 1
                if secondint == 0:
                    await message.edit(content="Ended!")
                    break
                
                await message.edit(content=f"Timer: {secondint}")
                await asyncio.sleep(1)
            await ctx.send(f"{tick} {ctx.author.mention}, Your countdown has been ended")
        except ValueError:
            await ctx.send(f"{cross} You must enter a number")

    @commands.command(hidden=True)
    @commands.bot_has_permissions(send_messages=True)
    async def colornum(self,ctx):
        colors = {
        "WHITE": 0xFFFFFF,
        "AQUA": 0x1ABC9C,
        "GREEN": 0x2ECC71,
        "BLUE": 0x3498DB,
        "PURPLE": 0x9B59B6,
        "LUMINOUS_VIVID_PINK": 0xE91E63,
        "GOLD": 0xF1C40F,
        "ORANGE": 0xE67E22,
        "RED": 0xE74C3C,
        "NAVY": 0x34495E,
        "DARK_AQUA": 0x11806A,
        "DARK_GREEN": 0x1F8B4C,
        "DARK_BLUE": 0x206694,
        "DARK_PURPLE": 0x71368A,
        "DARK_VIVID_PINK": 0xAD1457,
        "DARK_GOLD": 0xC27C0E,
        "DARK_ORANGE": 0xA84300,
        "DARK_RED": 0x992D22,
        "DARK_NAVY": 0x2C3E50,
        } 
        em = discord.Embed(description="__Color List__",color=await fetch_color(bot=self.bot,ctx=ctx))
        em.add_field(name=f"Here are all the list of colors available!",value=f"\n".join(f"Color name : {k} | Value : {v}" for k,v in colors.items()))
        em.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=em)

    # @commands.command(aliases=["dev"])
    # @commands.bot_has_permissions(send_messages=True)
    # async def developer(self,ctx):
    #     # await ctx.send("Scypher made me and I am ")
    #     # await ctx.send("https://media.tenor.co/videos/ee407e8a7a68a3612979b82e264812be/mp4")
    #     e = discord.Embed(title="About me",description="Scypher made me and I am ")
    #     e.video(url="https://media.tenor.co/videos/ee407e8a7a68a3612979b82e264812be/mp4")
    #     # e.add_field(name="Made in ",value="https://media.tenor.co/videos/ee407e8a7a68a3612979b82e264812be/mp4")
    #     # e.set_image(url="https://media.tenor.co/videos/ee407e8a7a68a3612979b82e264812be/mp4")
    #     await ctx.send(embed=e)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def repeat(self,ctx,*,msg):
        ''' Repeats a message '''
        await ctx.send(msg)

    # @commands.command()
    # @commands.bot_has_permissions(send_messages=True)
    # async def prepeat(self,ctx,*,msg):
    #     await ctx.channel.purge(limit=1)
    #     await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.bot_has_permissions(send_messages=True)
    async def mail(self,ctx,channel,*,message):
        if channel is None:
            return await ctx.send(f"{cross} Channel not found!")
        ch = discord.utils.get(self.bot.get_all_channels(),name=channel)
        await ch.send(message)
        await ctx.send(f"{tick} | Mail sent!")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def announce(self,ctx,channel:discord.TextChannel,*,message):
        ''' Announces a message in channel '''
        if channel is None:
            channel = message.channel
        await channel.send(message)
        await ctx.send(f"{tick} | Message has been announced to channel {channel}")

    @commands.command()
    async def links(self,ctx):
        ''' Get official links related to this bot '''
        em = discord.Embed(
            description=f"[Click here to get bot's invite link]({config.SUPPORT_SERVER_LINK})\n"
                        +f"[Click here to join supports server]({config.INVITE_LINK})",
        color=await fetch_color(bot=self.bot,ctx=ctx)
        )


def setup(bot):
    bot.add_cog(Message(bot))
    print(OKGREEN + "[STATUS OK] Message cog is ready")

