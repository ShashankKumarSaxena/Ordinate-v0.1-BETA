import discord
from discord.ext import commands
from cogs.utils.emoji import tick,cross
from colorama import Fore,init

init(autoreset=True)

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.bot.loop.create_task(self.setup())

    @commands.group(pass_context=True)
    @commands.bot_has_permissions(send_messages=True)
    async def afk(self, ctx):
        '''
        Set your afk status with this command.
        '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)
        
    
    @afk.command(pass_context=True)
    async def on(self, ctx):
        ''' To set afk status on without any message '''
        rec_flag = await self.bot.testdb1.fetchval("SELECT is_afk FROM userafk WHERE guild_id = $1 AND user_id = $2",ctx.guild.id,ctx.author.id)
        if rec_flag:
            # flag = rec_flag['is_afk']
            flag = rec_flag
            if flag:
                return await ctx.send(f"{cross} | You are already on afk in this server!")
        await self.bot.testdb1.execute("INSERT INTO userafk (user_id,guild_id,is_afk) VALUES ($1,$2,$3)",
                                        ctx.author.id,ctx.message.guild.id,True)
        await ctx.send(f"{tick} | I have set you on AFK")
    

    @afk.command(pass_context=True)
    async def set(self, ctx, *, content):
        ''' To set afk status on with a message. '''
        rec_flag = await self.bot.testdb1.fetchval("SELECT is_afk FROM userafk WHERE guild_id = $1 AND user_id = $2",ctx.guild.id,ctx.author.id)
        if rec_flag:
            # flag = rec_flag['is_afk']
            flag = rec_flag
            if flag:
                return await ctx.send(f"{cross} | You were already on afk in this server!")
        await self.bot.testdb1.execute("INSERT INTO userafk (user_id,guild_id,is_afk,afk_msg) VALUES ($1,$2,$3,$4)",
                                        ctx.author.id,ctx.message.guild.id,True,content)
        await ctx.send(f"{tick} | I have set you on AFK : {content}")

    @afk.command(pass_context=True)
    async def off(self,ctx):
        ''' Turn off your afk status. '''
        rec_flag = await self.bot.testdb1.fetchval("SELECT is_afk FROM userafk WHERE guild_id = $1 AND user_id = $2",ctx.guild.id,ctx.author.id)
        # flag = rec_flag['is_afk']
        flag = rec_flag
        if flag:
            await self.bot.testdb1.execute("DELETE FROM userafk WHERE guild_id = $1 AND user_id = $2",ctx.guild.id,ctx.author.id)
            await ctx.send(f"{tick} | I removed you from AFK successfully!")
        else:
            return await ctx.send(f"{cross} | You aren't AFK now")

    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS userafk (user_id bigint, guild_id bigint, is_afk boolean, afk_msg character varying, PRIMARY KEY (user_id,guild_id))")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()

    @commands.Cog.listener()
    async def on_message(self,message):
        if not message.guild or message.author.bot:
            return
        ctx = await self.bot.get_context(message)
        afk_user_ids_rec = await self.bot.testdb1.fetch("SELECT user_id FROM userafk WHERE guild_id = $1",message.guild.id)
        afk_user_ids = [r['user_id'] for r in afk_user_ids_rec]

        if not len(message.mentions) == 0:
            for user in message.mentions:
                if user.id in afk_user_ids:
                    afk_user = self.bot.get_user(user.id)
                    content = await self.bot.testdb1.fetchval("SELECT afk_msg FROM userafk WHERE guild_id = $1 AND user_id = $2",message.guild.id,int(user.id))
                    
                    if content is None:
                        await message.channel.send(f"{discord.utils.escape_markdown(message.author.name,as_needed=True,ignore_links=True)}, {discord.utils.escape_markdown(afk_user.name,as_needed=True,ignore_links=True)} is on AFK")
                    else:
                        # afk_msg = content['afk_msg']
                        afk_msg = content
                        await message.channel.send(
                            f"{discord.utils.escape_markdown(message.author.name,as_needed=True,ignore_links=True)}, {discord.utils.escape_markdown(afk_user.name,as_needed=True,ignore_links=True)} is on AFK"
                            + f"\nMessage : {afk_msg}"
                        )

        if message.author.id in afk_user_ids:
            user = self.bot.get_user(message.author.id)
            await self.bot.testdb1.execute("DELETE FROM userafk WHERE guild_id = $1 and user_id = $2",message.guild.id,user.id)
            await message.channel.send(f"Welcome back {user.mention}! Removing your AFK state.")
                


def setup(bot):
    bot.add_cog(Afk(bot))
    print(Fore.GREEN+"[STATUS OK] Afk cog is ready!")
