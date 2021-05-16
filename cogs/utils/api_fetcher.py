import requests
import json
import discord
from discord.ext import commands
import io
from cogs.utils.color import fetch_color
from functools import lru_cache # TO BE REMOVED

@lru_cache(maxsize=None)
def fetch_json(url):
    res = json.loads(requests.get(f"{url}").text)
    return res

@lru_cache(maxsize=None)
async def bytes_image(ctx,bot,url,user:discord.User=None):
    ''' This method will send the embed directly '''
    # print(url)
    res = requests.get(url)
    THMB = res.content
    stream = io.BytesIO(THMB)
    color = await fetch_color(bot=bot,ctx=ctx)
    e=discord.Embed(title=" ",color=color)
    file = discord.File(stream,'abc.png')
    e.set_image(url="attachment://abc.png")
    e.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=e,file=file)

@lru_cache(maxsize=None)
async def bytes_gif(ctx,bot,url,user:discord.User):
    ''' This method will send the embed directly '''
    # print(url)
    res = requests.get(url)
    THMB = res.content
    stream = io.BytesIO(THMB)
    color = await fetch_color(bot=bot,ctx=ctx)
    e=discord.Embed(title=" ",color=color)
    file = discord.File(stream,'abc.gif')
    e.set_image(url="attachment://abc.gif")
    e.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=e,file=file)

@lru_cache(maxsize=None)
async def bytes_image2(ctx,bot,url,user:discord.User,text):
    ''' This method will send the embed directly '''
    # print(url)
    res = requests.get(url)
    THMB = res.content
    stream = io.BytesIO(THMB)
    color = await fetch_color(bot=bot,ctx=ctx)
    e=discord.Embed(title=text,color=color)
    file = discord.File(stream,'abc.png')
    e.set_image(url="attachment://abc.png")
    e.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=e,file=file)