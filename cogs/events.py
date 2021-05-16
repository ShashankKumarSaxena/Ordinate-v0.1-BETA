import discord
from discord.ext import commands
from colorama import init,Fore
from cogs.utils.emoji import tick,qtick
import random

init(autoreset=True)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await self.bot.testdb1.execute("INSERT INTO guild_config (guild_id, welcomer, leaver, leveller, level_up_msg, nqnf) VALUES ($1,$2,$3,$4,$5,$6)",
                                        guild.id,False,False,False,True,False)

    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        # await ctx.message.add_reaction(tick)
        pass

        #============== TODO - Use it afterwards ============#
        # num = random.randint(1,100)
        # if num > 50:
        #     em = discord.Embed(description=f"It seems that you are enjoying using our bot {ctx.author.mention}. If you do then please vote for me.")
        #     await ctx.message.channel.send(embed=em)
        #====================================================#


def setup(bot):
    bot.add_cog(Events(bot))
    print(Fore.GREEN+"[STATUS OK] Events cog is ready!")
