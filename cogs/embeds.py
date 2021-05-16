import discord
from discord.ext import commands
import ast
import json
from cogs.utils.emoji import cross,tick

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Embeds(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(pass_context=True)
    # @commands.has_permissions(manage_messages=True)
    # @commands.bot_has_permissions(manage_messages=True)
    async def embeds(self,ctx):
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} To use this command - ")
            await ctx.send_help(helper)
    
    @embeds.command()
    # @commands.has_permissions(manage_messages=True)
    # @commands.bot_has_permissions(manage_messages=True)
    async def color(self,ctx,*,color):
        ''' Change the color of embeds. Enter only hex value of color '''
        # if type(color) is not hex:
        #     return await ctx.send("Please enter hex value of color!")
        nums = [0,1,2,3,4,5,6,7,8,9]
        if color.startswith("#"):
            color = color.replace("#","")
            color = "0x"+color
        elif color[0] in nums:
            return await ctx.send(f"{cross} | Please enter a valid hex value.")
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS colors(guild_id bigint,guild_name character varying,user_id bigint,user_name character varying,color bigint, PRIMARY KEY (guild_id,user_id))")
        # await self.bot.testdb1.execute("UPDATE colors SET color = $1 WHERE guild_id = $2",int("0x3498DB",0),ctx.guild.id) 
        color_if = await self.bot.testdb1.fetchrow("SELECT color FROM colors WHERE guild_id = $1",ctx.guild.id)
        if not color_if:
            try:
                color = int(color,0)
            except ValueError:
                return await ctx.send(f"{cross} | Please enter hex value starting with `#` or `0x`")
            await self.bot.testdb1.execute("INSERT INTO colors(guild_id,guild_name,user_id,user_name,color) VALUES ($1,$2,$3,$4,$5)",ctx.guild.id,ctx.guild.name,ctx.message.author.id,ctx.message.author.name,color)
            await ctx.send(f"{tick} | Color updated successfully!")
        else:
            # color = int(color,0)
            try:
                color = int(color,0)
            except ValueError:
                return await ctx.send(f"{cross} | Please enter hex value starting with `#` or `0x`")
            await self.bot.testdb1.execute("UPDATE colors SET color = $1 WHERE guild_id = $2",color,ctx.guild.id)
            # await ctx.send("Data updated successfully!")
            await ctx.send(f"{tick} | Color updated successfully!")


    # ========== TODO - Make it choice based ================#
    @embeds.command(hidden=True)
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def send(self,ctx,*,params):
        ''' Send a custom embed. Make sure to have data in JSON format '''
        # kw = ast.literal_eval(str(params))
        kw = json.loads(params)
        # print(kw)
        data = kw
        if 'description' in data:
            desc = data['description']
        else:
            return await ctx.send("Please enter a valid description! **Tip:** To make it none just enter a space in description.")
        if 'title' in data:
            title = data['title']
        else:
            title = None
        if 'image' in data:
            image = data['image']
        else:
            image=None
        if 'color' in data:
            color = data['color']
            color = int(color,0)
        else:
            color = discord.Color.default()
        try:
            if data['field'] is not None:
                name = data['field']['name']
                if 'field' in data and data['field']['name'] is None:
                    return await ctx.send("Please enter a valid field name")
                if 'field' in data and data['field']['value'] is not None:
                    value = data['field']['value']
                if 'value' in data and data['field']['value'] is None:
                    return await ctx.send("Please enter valid field value")
            else:
                pass
        except KeyError:
            pass
        
        if title:
            em = discord.Embed(title=title,description=desc,color=color)
        else:
            em = discord.Embed(description=desc)
        if image:
            em.set_thumbnail(url=image)
        try:
            if data['field']:
                em.add_field(name=name,value = value)
            else:
                pass
        except KeyError:
            pass
        else:
            pass

        await ctx.send(embed=em)

        #====================================================================#

    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS colors(guild_id bigint,guild_name character varying,user_id bigint,user_name character varying,color bigint, PRIMARY KEY (guild_id,user_id))")
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()


def setup(bot):
    bot.add_cog(Embeds(bot))
    print(OKGREEN + "[STATUS OK] Embed cog is ready!")