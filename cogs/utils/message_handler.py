import asyncio
import discord
from cogs.utils.color import fetch_color

async def GetMessage(
    bot,ctx,contentOne="Default",contentTwo=" ",timeout=100
):
    embed = discord.Embed(
        title=f"{contentOne}",
        description=f"{contentTwo}",
        color=await fetch_color(bot=bot,ctx=ctx)
    )
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            'message',
            timeout=timeout,
            check = lambda message: message.author == ctx.author
            and message.channel == ctx.channel,
        )
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False

async def getmsg(
    bot,ctx,question,timeout=100
):
    sent = await ctx.send(question)
    try:
        msg = await bot.wait_for('message',timeout=timeout,check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False