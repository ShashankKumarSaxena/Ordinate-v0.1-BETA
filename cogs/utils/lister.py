import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
import math
from cogs.utils.color import fetch_color

async def lister(ctx,your_list,color,*,title):
    pages = math.ceil(len(your_list)/15)
    page = [i for i in range(1,pages+1)]
    counts = []
    first_num = 0
    for i in page:
        if first_num == 0:
            last_num = (i*15) -1
        else:
            last_num = (i*15) -1
        if first_num > len(your_list):
            first_num = len(your_list)
        elif last_num > len(your_list):
            last_num = len(your_list)
        l = [first_num,last_num]
        counts.append(l)
        if last_num == len(your_list) or first_num == len(your_list):
            break
        first_num = last_num + 1
                        
    embeds = []
    
    for l in counts:
        first_num = l[0]
        last_num = l[1]
        em = discord.Embed(description=" ",color=color).add_field(name=f"{title} - [{len(your_list)}]",value="\n".join(f"`[{count+1}]` {your_list[count].mention}" for count in range(first_num,last_num)))
        embeds.append(em)
       
    paginator = BotEmbedPaginator(ctx,embeds)
    await paginator.run()


async def lister_str(ctx, your_list, color, *, title) -> None:
    pages = math.ceil(len(your_list) / 15)
    page = [i for i in range(1, pages + 1)]
    counts = []
    first_num = 0
    for i in page:
        if first_num == 0:
            last_num = (i * 15) - 1
        else:
            last_num = (i * 15) - 1
        if first_num > len(your_list):
            first_num = len(your_list)
        elif last_num > len(your_list):
            last_num = len(your_list)
        l = [first_num, last_num]
        counts.append(l)
        if last_num == len(your_list) or first_num == len(your_list):
            break
        first_num = last_num + 1

    embeds = []

    for l in counts:
        first_num = l[0]
        last_num = l[1]
        em = discord.Embed(description=" ", color=color).add_field(name=f"{title} - [{len(your_list)}]",
                                                                   value="\n".join(
                                                                       f"`[{count + 1}]` {your_list[count]}" for
                                                                       count in range(first_num, last_num)))
        embeds.append(em)

    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()