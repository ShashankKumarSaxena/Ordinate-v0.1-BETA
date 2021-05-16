import discord
from discord.ext import commands
import asyncio
from cogs.utils.emoji import qtick,qcross,cross

async def confirmation(ctx,bot,*,msg):
    await ctx.send(msg)
    msg = await ctx.send("**Are you sure you want to continue?**")
    await msg.add_reaction(qtick)
    await msg.add_reaction(qcross)
    channel = ctx.message.channel
    def check(reaction,user):
        return user == ctx.message.author and str(reaction.emoji) in [qtick,qcross]
    try:
        reaction,user = await bot.wait_for('reaction_add',timeout=60.0,check=check)
    except asyncio.TimeoutError:
            await channel.send(f"{cross} | Task was cancelled due to timeout.")
    else:
        # await channel.send(reaction.emoji)
        return reaction.emoji