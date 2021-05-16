import discord
from discord.ext import commands
import re
import random
from cogs.utils.message_handler import GetMessage
from cogs.utils.emoji import cross,tick,qtick,qcross
from cogs.utils.color import fetch_color
from cogs.utils.confimation import confirmation
import asyncio
from colorama import init,Fore

init(autoreset=True)

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600,"s":1,"m":60,"d":86400}

def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key,value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)

class Giveaway(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(
        name='giveaway'
    )
    @commands.bot_has_guild_permissions(send_messages=True)
    async def _start(self,ctx):
        ''' Host a giveaway with this command '''
        await ctx.send(f"Lets setup the giveaway, just answer the questions which I will be asking to you.")
        question_list = [
            ["What channel do you want the giveaway to be in?","Mention the channel"],
            ["How long should the giveaway last","Please specify the time in format `s|m|h|d`"],
            ["What should be the prize for the giveaway?","Please enter the prize for the giveaway!"]
        ]
        answers = {}
        for i, question in enumerate(question_list):
            answer = await GetMessage(self.bot,ctx,question[0],question[1])
            if not answer:
                return await ctx.send(f"{cross} | You failed to answer, please answer quicker next time.")
            answers[i] = answer
        embed = discord.Embed(
            name="Giveaway setup",
            color = await fetch_color(bot=self.bot,ctx=ctx)
        )
        for key,value in answers.items():
            embed.add_field(name=f"{question_list[key][0]}",value=f"{value}",inline=False)
        await ctx.send(embed=embed)
        reaction = await confirmation(ctx=ctx,bot=self.bot,msg="Is the entered data valid?")
        if reaction.name == "qcross":
            return await ctx.send(f"{cross} | Giveaway cancelled!")
        channelId = re.findall(r"[0-9]+",answers[0])[0]
        channel = self.bot.get_channel(int(channelId))
        time = convert(answers[1])
        giveawayEmbed = discord.Embed(
            title="🎉 **Giveaway** 🎉",
            description = "||  ||" + "**Prize**: " + answers[2],
            color = await fetch_color(bot=self.bot,ctx=ctx)
        )
        giveawayEmbed.set_footer(text=f"The giveaway ends {time} seconds from this message.")
        giveawayMessage = await channel.send(embed=giveawayEmbed)
        await giveawayMessage.add_reaction("🎉")
        await ctx.send(f"{tick} | Giveaway hosted successfully!")
        await asyncio.sleep(time)
        message = await channel.fetch_message(giveawayMessage.id)
        users = await message.reactions[0].users().flatten()
        users.pop(users.index(ctx.guild.me))
        if len(users) == 0:
            return await channel.send(f"{cross} | No winner was decided")
        winner = random.choice(users)
        await channel.send(f"🎉 **Congratulations {winner.mention}! You won the giveaway.**\nPlease contact {ctx.author.mention} about your prize.")


def setup(bot):
    bot.add_cog(Giveaway(bot))
    print(Fore.GREEN+"[STATUS OK] Giveaway cog is ready!")
