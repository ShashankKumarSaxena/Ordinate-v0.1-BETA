import discord
from discord.ext import commands
from cogs.utils.color import fetch_color
from functools import lru_cache

@lru_cache(maxsize=None)
async def basic1(ctx,bot,title:str=None,description:str=None):
    color = await fetch_color(bot=bot,ctx=ctx)
    em = discord.Embed(title=title,description=description,color=color)
    em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    return em

@lru_cache(maxsize=None)
async def basic_image1(ctx,bot,image_url):
    color = await fetch_color(bot=bot,ctx=ctx)
    em = discord.Embed(description=" ",color=color)
    em.set_image(url=image_url)
    em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    return em

@lru_cache(maxsize=None)
async def basic_image2(ctx,bot,image_url,text:str):
    color = await fetch_color(bot=bot,ctx=ctx)
    em = discord.Embed(title=text,description=" ",color=color)
    em.set_image(url=image_url)
    em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    return em