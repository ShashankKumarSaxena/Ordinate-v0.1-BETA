import discord
from discord.ext import commands
from cogs.utils.emoji import tick,cross
from colorama import init,Fore
from cogs.utils.color import fetch_color2
import datetime

init(autoreset=True)

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #==========================================================================JOIN ROLE ==============================================================================
    
    @commands.command(aliases=['joinrole'])
    @commands.has_permissions(administrator=True)
    async def onjoinrole(self,ctx,role:discord.Role):
        await self.bot.testdb1.execute("UPDATE guild_config SET on_join_role = $1 WHERE guild_id = $2", role.id, ctx.guild.id)
        await ctx.send(f"{tick} | New members will get the role {role.mention} on server join!")

    @commands.command(aliases=['removejoinrole'])
    @commands.has_permissions(administrator=True)
    async def removeonjoinrole(self,ctx):
        await self.bot.testdb1.execute("UPDATE guild_config SET on_join_role = null WHERE guild_id = $1",ctx.guild.id)
        await ctx.send(f"{tick} | Successfully removed the role.")


    #=================================================================================================================================================================

    #==========================================================================WELCOMER ==============================================================================

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def welcomer(self, ctx, channel:discord.TextChannel=None, *, msg=None):
        channel = channel or ctx.message.channel
        flag = await self.bot.testdb1.fetchval("SELECT welcomer FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        prev_channel = await self.bot.testdb1.fetchval("SELECT welcomer_channel FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        prev_msg = await self.bot.testdb1.fetchval("SELECT welcomer_msg FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if prev_channel is None:
            await self.bot.testdb1.execute("UPDATE guild_config SET welcomer = $1, welcomer_channel = $2, welcomer_msg = $4 WHERE guild_id = $3",
                                           True, channel.id, ctx.guild.id, msg)
            await ctx.send(f"{tick} | Successfully enabled welcomer! You will recieve welcomes in {channel.mention}")
        elif flag is True and prev_channel == channel.id:
            await self.bot.testdb1.execute("UPDATE guild_config SET welcomer = $1 WHERE guild_id = $2",False,ctx.guild.id)
            await ctx.send(f"{tick} | Successfully disabled welcomer!")
        elif flag is True and prev_channel != channel.id:
            await self.bot.testdb1.execute("UPDATE guild_config SET welcomer_channel = $1, msg = $3 WHERE guild_id = $2",
                                           channel.id, ctx.guild.id, msg)
            await ctx.send(f"{tick} | Successfully updated welcomer channel to {channel.mention}")
        elif flag is False:
            await self.bot.testdb1.execute("UPDATE guild_config SET welcomer = $1, welcomer_channel = $2, welcomer_msg = $4 WHERE guild_id = $3",
                                            True, channel.id, ctx.guild.id, msg)
            await ctx.send(f"{tick} | Successfully enabled welcomer! You will recieve welcomes in {channel.mention}")
        elif flag is True and msg != prev_msg:
            await self.bot.testdb1.execute("UPDATE guild_config SET welcomer_msg = $1 WHERE guild_id = $2",msg,ctx.guild.id)
            await ctx.send(f"{tick} | Updated welcome message successfully!")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_id = await self.bot.testdb1.fetchval("SELECT on_join_role FROM guild_config WHERE guild_id = $1",member.guild.id)
        if role_id is not None:
            role = member.guild.get_role(role_id)
            await member.add_roles(role)

        flag = await self.bot.testdb1.fetchval("SELECT welcomer FROM guild_config WHERE guild_id = $1",
                                               member.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT welcomer_channel FROM guild_config WHERE guild_id = $1",member.guild.id)
            channel = self.bot.get_channel(chid)
            msg = await self.bot.testdb1.fetchval("SELECT welcomer_msg FROM guild_config WHERE guild_id = $1",member.guild.id)
            msg = msg or " "
            em = discord.Embed(
                title=f"Welcome {member.name} to {member.guild.name}",
                description=f"{msg}",
                color=await fetch_color2(bot=self.bot,guild_id=member.guild.id)
            )
            await channel.send(embed=em)
        
    
    #=================================================================================================================================================================

    #==========================================================================LEAVER ==============================================================================

    @commands.command(aliases=['leaver','lefter'])
    @commands.has_permissions(administrator=True)
    async def wishgoodbye(self, ctx, channel:discord.TextChannel=None, *, msg=None):
        channel = channel or ctx.message.channel
        flag = await self.bot.testdb1.fetchval("SELECT leaver FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        prev_channel = await self.bot.testdb1.fetchval("SELECT leaver_channel FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        prev_msg = await self.bot.testdb1.fetchval("SELECT leaver_msg FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        if prev_channel is None:
            await self.bot.testdb1.execute("UPDATE guild_config SET leaver = $1, leaver_channel = $2, leaver_msg = $4 WHERE guild_id = $3",
                                           True, channel.id, ctx.guild.id, msg)
            await ctx.send(f"{tick} | Successfully enabled leave logs! You will recieve it in {channel.mention}")
        elif flag is True and prev_channel == channel.id:
            await self.bot.testdb1.execute("UPDATE guild_config SET leaver = $1 WHERE guild_id = $2",False,ctx.guild.id)
            await ctx.send(f"{tick} | Successfully disabled wishing goodbye!")
        elif flag is True and prev_channel != channel.id:
            await self.bot.testdb1.execute("UPDATE guild_config SET leaver_channel = $1, msg = $3 WHERE guild_id = $2",
                                           channel.id, ctx.guild.id, msg)
            await ctx.send(f"{tick} | Successfully updated leaver channel to {channel.mention}")
        elif flag is False:
            await self.bot.testdb1.execute("UPDATE guild_config SET leaver = $1, leaver_channel = $2, leaver_msg = $4 WHERE guild_id = $3",
                                            True, channel.id, ctx.guild.id, msg)
            await ctx.send(f"{tick} | Successfully enabled goodbye wisher! You will recieve messages in {channel.mention}")
        elif flag is True and msg != prev_msg:
            await self.bot.testdb1.execute("UPDATE guild_config SET leaver_msg = $1 WHERE guild_id = $2",msg,ctx.guild.id)
            await ctx.send(f"{tick} | Updated goodbye message successfully!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        flag = await self.bot.testdb1.fetchval("SELECT leaver FROM guild_config WHERE guild_id = $1",
                                               member.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT leaver_channel FROM guild_config WHERE guild_id = $1",member.guild.id)
            channel = self.bot.get_channel(chid)
            msg = await self.bot.testdb1.fetchval("SELECT leaver_msg FROM guild_config WHERE guild_id = $1",member.guild.id)
            msg = msg or " "
            em = discord.Embed(
                title=f"Bye {member.name}.",
                description=f"{msg}",
                color=await fetch_color2(bot=self.bot,guild_id=member.guild.id),
            )
            await channel.send(embed=em)

    #=================================================================================================================================================================

    #========================================================================== LOGGING ==============================================================================

    @commands.command()
    async def modlogs(self,ctx,channel:discord.TextChannel=None):
        channel = channel or ctx.message.channel
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",ctx.guild.id)
        prev_channel = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",ctx.guild.id)

        if prev_channel is None:
            await self.bot.testdb1.execute("UPDATE guild_config SET mod_logs = $1, mod_logs_channel = $2 WHERE guild_id = $3",
                                            True, channel.id, ctx.guild.id)
            await ctx.send(f"{tick} | Successfully enabled mod-logs! You will recieve them in {channel.mention}")
        elif flag is True and prev_channel == channel.id:
            await self.bot.testdb1.execute("UPDATE guild_config SET mod_logs = $1 WHERE guild_id = $2",False, ctx.guild.id)
            await ctx.send(f"{tick} | Successfully disabled mod-logs!")
        elif flag is True and prev_channel != channel.id:
            await self.bot.testdb1.execute("UPDATE guild_config SET mod_logs_channel = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
            await ctx.send(f"{tick} | Successfully updated mod-logs channel to {channel.mention}!")
        elif flag is False:
            await self.bot.testdb1.execute("UPDATE guild_config SET mod_logs = $1, mod_logs_channel = $2 WHERE guild_id = $3",
                                            True, channel.id, ctx.guild.id)
            await ctx.send(f"{tick} | Successfully enabled mod-logs! You will recieve them in {channel.mention}.")


    @commands.Cog.listener()
    async def on_member_ban(self,guild,member):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                description=f"{member.name} has been banned from this server!",
                color=await fetch_color2(bot=self.bot,guild_id=guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            await modlogchannel.send(embed=em)


    @commands.Cog.listener()
    async def on_member_unban(self,guild,member):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                description=f"{member.name} has been unbanned from this server!",
                color=await fetch_color2(bot=self.bot,guild_id=guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            await modlogchannel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        pass

    @commands.Cog.listener()
    async def on_bulk_message_delete(self,messages):
        pass
    

    #============================== FOR SUPPORT SERVER ================================#
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        pass

    #==================================================================================#


    @commands.Cog.listener()
    async def on_guild_update(self,before,after):
        pass

    @commands.Cog.listener()
    async def on_guild_role_create(self,role):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",role.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",role.guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                description=f"{role.name} has been created!",
                color=await fetch_color2(bot=self.bot,guild_id=role.guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            await modlogchannel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",role.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",role.guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                description=f"{role.name} has been deleted!",
                color=await fetch_color2(bot=self.bot,guild_id=role.guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            await modlogchannel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_update(self,before,after):
        pass

    @commands.Cog.listener()
    async def on_guild_emojis_update(self,guild,before,after):
        pass

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",message.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",message.guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                color=await fetch_color2(bot=self.bot,guild_id=message.guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            em.add_field(name="__Deleted Message Content__",value=message.content)
            await modlogchannel.send(embed=em)
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",channel.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",channel.guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                description=f"New channel created - {channel.mention}",
                color=await fetch_color2(bot=self.bot,guild_id=channel.guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            await modlogchannel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        flag = await self.bot.testdb1.fetchval("SELECT mod_logs FROM guild_config WHERE guild_id = $1",channel.guild.id)
        if flag is True:
            chid = await self.bot.testdb1.fetchval("SELECT mod_logs_channel FROM guild_config WHERE guild_id = $1",channel.guild.id)
            modlogchannel = self.bot.get_channel(chid)
            em = discord.Embed(
                title="Mod Logs",
                description=f"Channel deleted - {channel.name}",
                color=await fetch_color2(bot=self.bot,guild_id=channel.guild.id),
                timestamp=datetime.datetime.utcnow()
            )
            await modlogchannel.send(embed=em)

    @commands.Cog.listener()
    async def on_webhook_update(self, channel):
        pass

    #=================================================================================================================================================================

    async def setup(self):
        pass

def setup(bot):
    bot.add_cog(Logs(bot))
    print(Fore.GREEN + "[STATUS OK] Logs cog is ready!")
