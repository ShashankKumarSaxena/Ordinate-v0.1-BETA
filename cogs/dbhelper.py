import discord
from discord.ext import commands
import dump
import os
import sys
from colorama import init,Fore
import subprocess

init(autoreset=True)

class DBHelp(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        #======== Database initialization =============#
        # self.testdb1 = bot.testdb1
        #==============================================#

    @commands.group(pass_context=True)
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def db(self,ctx):
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} To use this command - ")
            await ctx.send_help(helper)

    @db.command()
    @commands.is_owner()
    async def backup(self,ctx):
        em1 = discord.Embed(title="Creating backup ...",description="Database backup is in progress please wait")
        em2 = discord.Embed(title="Backup successfull!",description="Database backup successfull!")
        msg = await ctx.send(embed=em1)
        try:
            os.system(f"pg_dump -d discordtest1 -f testbck1.sql -U postgres -W") # USE URI
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=e))
        await msg.edit(embed=em2)

    @db.command()
    @commands.is_owner()
    async def restore(self, ctx):
        pass


def setup(bot):
    bot.add_cog(DBHelp(bot))
    print(Fore.GREEN + "[STATUS OK] DBHelp cog is ready!")
