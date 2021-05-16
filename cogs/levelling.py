import discord
from discord.ext import commands
import math
import random
from cogs.utils.emoji import tick,cross
from colorama import init,Fore
from cogs.utils.color import fetch_color
from cogs.utils.lister import lister_str

init(autoreset=True)

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    Full logic for levelling system -

    To calculate level -
    ((xp - 20) / 40) + 1 = level
    
    To show level = ceil(level)

    To calculate xp-
    xp = 20 + (level - 1) * 40
    '''

    async def register_user(self, user:discord.Member, guild_id:int, level:int, xp:int):
        await self.bot.testdb1.execute("INSERT INTO levelling (guild_id,user_id,level,xp) VALUES ($1, $2, $3, $4)",
                                        guild_id,user.id,level,xp)
    
    async def fetch_data(self, user:discord.Member) -> tuple:
        rec_result = await self.bot.testdb1.fetch("SELECT * FROM levelling WHERE user_id = $1 AND guild_id = $2",
                                                    user.id, user.guild.id)
        
        if not rec_result:
            await self.register_user(user=user,guild_id=user.guild.id,level=0,xp=0)
            return (user.guild.id, user.id, 0, 0)
        

        result = (rec_result[0]['guild_id'],rec_result[0]['user_id'],rec_result[0]['level'],rec_result[0]['xp'])

        return result

    def calculate_xp(self, level:int):
        xp = 20 + (level - 1) * 40
        return xp

    def calculate_level(self, xp:int):
        level = ((xp - 20) / 40) + 1
        return level

    @commands.group(pass_context=True)
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    async def levelling(self,ctx):
        ''' Levelling per message in a server '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    @levelling.command(pass_context=True)
    async def enable(self,ctx):
        ''' Enable levelling in your server '''
        flag = await self.bot.testdb1.fetchval("SELECT leveller FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if flag is False:
            await self.bot.testdb1.execute("UPDATE guild_config SET leveller = $1 WHERE guild_id = $2",
                                            True, ctx.guild.id)
            await ctx.send(f"{tick} | Levelling successfully enabled for this guild!")
        else:
            return await ctx.send(f"{tick} | Levelling is already enabled for this server!")

    @levelling.command(pass_context=True)
    async def disable(self,ctx):
        ''' Disable levelling in your server '''
        flag = await self.bot.testdb1.fetchval("SELECT leveller FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if flag is True:
            await self.bot.testdb1.execute("UPDATE guild_config SET leveller = $1 WHERE guild_id = $2",
                                            False, ctx.guild.id)
            await ctx.send(f"{tick} | Levelling successfully disabled for this server!")
        else:
            return await ctx.send(f"{cross} | Levelling is already disabled for this server.")

    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS levelling (guild_id bigint, user_id bigint, level integer, xp integer)")

    @levelling.command(pass_context=True)
    async def levelupmsg(self,ctx):
        ''' Toggle level up message. '''
        flag = await self.bot.testdb1.fetchval("SELECT level_up_msg FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if flag is True:
            await self.bot.testdb1.execute("UPDATE guild_config SET level_up_msg = $1 WHERE guild_id = $2",
                                            False, ctx.guild.id)
            await ctx.send(f"{tick} | Level up messages are now disabled for this server!")
        else:
            await self.bot.testdb1.execute("UPDATE guild_config SET level_up_msg = $1 WHERE guild_id = $2",
                                            True, ctx.guild.id)
            await ctx.send(f"{tick} | Level up messages are now enabled for this server!")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild is None:
            return
        flag = await self.bot.testdb1.fetchval("SELECT leveller FROM guild_config WHERE guild_id = $1",message.guild.id)
        if flag is True:
            if message.author.bot or message.guild is None:
                return
            
            data = await self.fetch_data(user=message.author)
            # data format (guild_id, user_id, level, xp)

            guild_id, user_id, level, xp = data

            xp += random.randint(1,7)
            await self.bot.testdb1.execute("UPDATE levelling SET xp = $1 WHERE guild_id = $2 AND user_id = $3",
                                            xp, message.guild.id, message.author.id)

            l = self.calculate_level(xp)
            if round(l) > level and round(l) != 0:
                await self.bot.testdb1.execute("UPDATE levelling set level = $1,xp = $4 WHERE guild_id = $2 AND user_id = $3",
                                                round(l), message.guild.id, message.author.id,0)
                flg = await self.bot.testdb1.fetchval("SELECT level_up_msg FROM guild_config WHERE guild_id = $1",message.guild.id)
                if flg is True:
                    try:
                        await message.channel.send(f"Congratulations {message.author.mention}! You advanced to level {round(l)}",
                                                    allowed_mentions=discord.AllowedMentions(users=False))
                    except:
                        await message.author.send(f"Congratulations {message.author.mention}! You advanced to level {round(l)} in {message.guild.name}!")

        else:
            return

    def get_progress_bar(self,bar_length:int,items:int):
        spaces = int(bar_length - items) # left

        to_be_printed = ""

        for _ in range(1,bar_length):
            the_hashes = "".join("█" for i in range(1,items))
            # the_hashes = "".join("#" for i in range(1,items))
            space_print = "".join(" " for j in range(1,spaces))
            
        to_be_printed = to_be_printed + f"[{the_hashes}{space_print}]"
        return to_be_printed
    
    @commands.command(aliases=['rank',])
    async def level(self,ctx,user:discord.Member=None):
        ''' Check your level and progress '''
        user = user or ctx.author
        em = discord.Embed(
            title=f"Level & Rank of {user.name}",
            color = await fetch_color(bot=self.bot,ctx=ctx)
        )
        level = await self.bot.testdb1.fetchval("SELECT level FROM levelling WHERE guild_id = $1 AND user_id = $2",
                                                ctx.guild.id,user.id)
        if level is None:
            return await ctx.send(f"{cross} | You don't have any levels now.")
        xp = await self.bot.testdb1.fetchval("SELECT xp FROM levelling WHERE guild_id = $1 AND user_id = $2",
                                                ctx.guild.id,user.id)
        total_xp = self.calculate_xp(level + 1)

        r_rank = await self.bot.testdb1.fetchval("SELECT COUNT(*) FROM levelling WHERE guild_id = $1 AND user_id = $2",
                                                    ctx.guild.id,user.id)

        data = await self.bot.testdb1.fetch("SELECT * FROM levelling ORDER BY level DESC")
            
        rec_leaderboard_data = []
        for d in data:
            if ctx.guild.id == d['guild_id']:
                rec_leaderboard_data.append(d)

            leaderboard_data = []
            for ld in rec_leaderboard_data:
                leaderboard_data.append(ld['user_id'])
        
        rank = leaderboard_data.index(ctx.author.id)

        em.add_field(name="Your stats ",value=f"```ruby\n"
                                                +f"Level: {level}\n"
                                                +f"Rank: {rank + 1}\n"
                                                +f"XP: {xp} / {total_xp}\n"
                                                +f"```")
                                                
        xp50 = int((xp / total_xp) * 20)
        em.add_field(name="Progress",value=f"```{self.get_progress_bar(bar_length=20,items=int(xp50))}```",inline=False)
        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    async def leaderboard(self,ctx):
        ''' Shows the leaderboard of your server according to levels '''
        flag = await self.bot.testdb1.fetchval("SELECT leveller FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if flag is True:
            data = await self.bot.testdb1.fetch("SELECT * FROM levelling ORDER BY level DESC")
            
            rec_leaderboard_data = []
            for d in data:
                if ctx.guild.id == d['guild_id']:
                    rec_leaderboard_data.append(d)

            leaderboard_data = []
            for ld in rec_leaderboard_data:
                leaderboard_data.append(f"{self.bot.get_user(ld['user_id']).name} `{ld['user_id']}`")
            
            await lister_str(ctx=ctx,
                            your_list=leaderboard_data,
                            color=await fetch_color(bot=self.bot,ctx=ctx),
                            title=f":medal: Leaderboard of {ctx.guild.name} :medal:")
        else:
            return await ctx.send(f"{cross} | Levelling is disabled for this server!")

    @commands.command()
    @commands.is_owner()
    async def give_xp(self,ctx,user:discord.Member,xp:int):
        await self.bot.testdb1.execute(f"UPDATE levelling SET xp = $3 WHERE user_id = $1 AND guild_id = $2",
                                        user.id,ctx.guild.id,xp)
        await ctx.send(f"{tick} | XP given to user successfully!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()

def setup(bot):
    bot.add_cog(Levelling(bot))
    print(Fore.GREEN + "[STATUS OK] Levelling cog is ready!")
