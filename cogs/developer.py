import discord
from discord.ext import commands
import traceback

class Develop(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # @commands.command(aliases=["tb"])
    # @commands.is_owner()
    # @commands.bot_has_permissions(send_messages=True)
    # async def traceback(self,ctx,flag=None):
    #     tr = traceback.format_exc()
    #     if tr is not None:
    #         if flag == 1:
    #             await ctx.send(f"```py\n{tr}\n```")
    #         else:
    #             # await owner.send(f"```py\n{tr}\n```")
    #             pass
    #     else:
    #         await ctx.send("Nothing to show now")




def setup(bot):
    bot.add_cog(Develop(bot))
    print("developer cog is ready")