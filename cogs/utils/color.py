import discord
from discord.ext import commands

async def fetch_color(bot,ctx):
    color = await bot.testdb1.fetchval("SELECT color FROM colors WHERE guild_id = $1",ctx.guild.id)
    if not color:
        return discord.Color.orange()
    else:
        return int(color)

async def fetch_color2(bot,guild_id:int):
    color = await bot.testdb1.fetchval("SELECT color FROM colors WHERE guild_id = $1",guild_id)
    if not color:
        return discord.Color.orange()
    else:
        return int(color)