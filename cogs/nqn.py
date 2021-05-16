from discord.ext import commands
# from redbot.core import commands
from discord import utils
import discord
import json
import sys
from colorama import init, Fore
from cogs.utils import emoji

init(autoreset=True)


class NQN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def nqn(self, ctx):
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} To use this command - ")
            await ctx.send_help(helper)
        # pass

    @nqn.command(pass_context=True)
    async def enable(self, ctx):
        ''' Enable notquitenitro (nqn) for server'''
        flag = await self.bot.testdb1.fetchval("SELECT nqnf FROM guild_config WHERE guild_id = $1", ctx.guild.id)
        if flag is True:
            return await ctx.send(f"{emoji.tick} | NQN is already enabled for this server!")

        else:
            await self.bot.testdb1.execute('UPDATE guild_config SET nqnf = $1 WHERE guild_id = $2',
                                           True, ctx.guild.id)
            await ctx.send(f"{emoji.tick} | NQN successfully enabled for this server!")

    @nqn.command(pass_context=True)
    async def disable(self, ctx):
        ''' Disable notquitenitro (nqn) for server'''
        flag = await self.bot.testdb1.fetchval("SELECT nqnf FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if flag is False:
            return await ctx.send(f"{emoji.cross} | NQN is already disabled for this server!")
        else:
            await self.bot.testdb1.execute("UPDATE guild_config SET nqnf = $1 WHERE guild_id = $2",
                                           False, ctx.guild.id)
            await ctx.send(f"{emoji.tick} | NQN successfully disabled for this server!")

    async def getemote(self, arg):
        emoji = utils.get(self.bot.emojis, name=arg.strip(":"))

        if emoji is not None:
            if emoji.animated:
                add = "a"
            else:
                add = ""
            return f"<{add}:{emoji.name}:{emoji.id}>"
        else:
            return None

    async def getinstr(self, content):
        ret = []

        spc = content.split(" ")
        cnt = content.split(":")

        if len(cnt) > 1:
            for item in spc:
                if item.count(":") > 1:
                    wr = ""
                    if item.startswith("<") and item.endswith(">"):
                        ret.append(item)
                    else:
                        cnt = 0
                        for i in item:
                            if cnt == 2:
                                aaa = wr.replace(" ", "")
                                ret.append(aaa)
                                wr = ""
                                cnt = 0

                            if i != ":":
                                wr += i
                            else:
                                if wr == "" or cnt == 1:
                                    wr += " : "
                                    cnt += 1
                                else:
                                    aaa = wr.replace(" ", "")
                                    ret.append(aaa)
                                    wr = ":"
                                    cnt = 1

                        aaa = wr.replace(" ", "")
                        ret.append(aaa)
                else:
                    ret.append(item)
        else:
            return content

        return ret

    # i added extra indent by mistake -_-

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        flag = await self.bot.testdb1.fetchval("SELECT nqnf FROM guild_config WHERE guild_id = $1",message.guild.id)
        try:
            if flag:
                if message.author.bot:
                    return

                if ":" in message.content:
                    msg = await self.getinstr(message.content)
                    ret = ""
                    em = False
                    smth = message.content.split(":")
                    if len(smth) > 1:
                        for word in msg:
                            if word.startswith(":") and word.endswith(":") and len(word) > 1:
                                emoji = await self.getemote(word)
                                if emoji is not None:
                                    em = True
                                    ret += f" {emoji}"
                                else:
                                    ret += f" {word}"
                            else:
                                ret += f" {word}"

                    else:
                        ret += msg

                    if em:
                        webhooks = await message.channel.webhooks()
                        webhook = utils.get(webhooks, name="Ordinate | NQN")
                        if webhook is None:
                            webhook = await message.channel.create_webhook(name="Ordinate | NQN")

                        await webhook.send(ret, username=message.author.name, avatar_url=message.author.avatar_url)
                        await message.delete()
        except KeyError:
            pass


def setup(bot):
    bot.add_cog(NQN(bot))
    print(Fore.GREEN + "[STATUS OK] NQN cog is ready!")
