# TODO - This file is temporary and will be removed in a future release

import discord
from discord.ext import commands
import asyncpg
import asyncio
from cogs.utils.emoji import qtick,qcross

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class TestDb(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    # RAW QUERY 
    # CREATE TABLE public."testA"
    # (
    # guild_id bigint,
    # guild_name character varying,
    # user_id bigint,
    # user_name character varying,
    # color bigint,
    # PRIMARY KEY (guild_id, user_id)
    # );

    
           

    @commands.command()
    async def insert(self,ctx,*,color:int):
        if type(color) is not int:
            return await ctx.send("Please give a valid color!")
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS testtable(guild_id bigint,guild_name character varying,user_id bigint,user_name character varying,color bigint, PRIMARY KEY (guild_id,user_id))")
        color_if = await self.bot.testdb1.fetchrow("SELECT color FROM testtable WHERE guild_id = $1",ctx.guild.id)
        if not color_if:
            await self.bot.testdb1.execute("INSERT INTO testtable(guild_id,guild_name,user_id,user_name,color) VALUES ($1,$2,$3,$4,$5)",ctx.guild.id,ctx.guild.name,ctx.message.author.id,ctx.message.author.name,color)
            await ctx.send("Data inserted successfully!")
        else:
            await self.bot.testdb1.execute("UPDATE testtable SET color = $1 WHERE guild_id = $2",color,ctx.guild.id)
            await ctx.send("Data updated successfully!")

    @commands.command()
    async def fcolor(self,ctx):
        color = await self.bot.testdb1.fetchval("SELECT color FROM testtable WHERE guild_id = $1",ctx.guild.id)
        await ctx.send(color)


    @commands.command()
    async def confirmation(self,ctx):
        msg = await ctx.send("Are you sure about that?")
        await msg.add_reaction(qtick)
        await msg.add_reaction(qcross)
        channel = ctx.message.channel
        def check(reaction,user):
            return user == ctx.message.author and str(reaction.emoji) in [qtick,qcross]

        try:
            reaction,user = await self.bot.wait_for('reaction_add',timeout=60.0,check=check)
        except asyncio.TimeoutError:
            await channel.send("Time up")
        else:
            await channel.send(reaction)    
    
    


def setup(bot):
    bot.add_cog(TestDb(bot))
    print(OKGREEN + "[STATUS OK] Database cog is ready!")
    

