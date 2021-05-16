import discord
from discord.ext import commands
from colorama import Fore,init
from cogs.utils.emoji import tick,cross
from cogs.utils.color import fetch_color

init(autoreset=True)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.bot.loop.create_task(self.setup())
    
    @commands.command(aliases=['rr'])
    @commands.bot_has_permissions(
        send_messages=True,
        add_reactions=True
    )
    async def reactionrole(self, ctx, msg_id:int, role:discord.Role, emoji:discord.Emoji):
        ''' Setup reaction roles for any message '''
        msg = await ctx.fetch_message(msg_id)
        await self.bot.testdb1.execute("INSERT INTO reactionroles (guild_id,msg_id,role,emoji) VALUES ($1,$2,$3,$4)",ctx.guild.id,msg_id,role.id,emoji.id)
        await msg.add_reaction(emoji)
        await ctx.send(f"{tick} | Reaction roles are successfully setup!")

    @commands.command(aliases=['rr_remove'])
    async def reactonroleremove(self,ctx,*,message_id=None):
        ''' Remove reaction roles from any message '''
        if message_id is None:
            await self.bot.testdb1.execute("DELETE FROM reactionroles WHERE guild_id = $1",ctx.guild.id)
        else:
            message_id = int(message_id)
            await self.bot.testdb1.execute("DELETE FROM reactionroles WHERE guild_id = $1 AND msg_id = $2",ctx.guild.id,message_id)
        await ctx.send(f"{tick} | Reaction roles successfully deleted!")

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        guild_id = reaction.message.guild.id
        msg_ids = role_ids = emoji_ids = []
        msg_ids_rec = role_ids_rec = emoji_names_rec = []

        msg_ids_rec = await self.bot.testdb1.fetch("SELECT msg_id FROM reactionroles WHERE guild_id = $1",guild_id)
        msg_ids = [m['msg_id'] for m in msg_ids_rec]

        for msg_id in msg_ids:
            role_ids.append(await self.bot.testdb1.fetchval("SELECT role FROM reactionroles WHERE guild_id = $1 AND msg_id = $2",guild_id,int(msg_id)))
            emoji_ids.append(await self.bot.testdb1.fetchval("SELECT emoji FROM reactionroles WHERE guild_id = $1 AND msg_id = $2",guild_id,int(msg_id)))
        
        fguild = self.bot.get_guild(int(guild_id))

        try:
            if reaction.emoji.id in emoji_ids and reaction.message.id in msg_ids:
                rid = await self.bot.testdb1.fetchval("SELECT role FROM reactionroles WHERE emoji = $1 AND msg_id = $2"
                                                    ,reaction.emoji.id,reaction.message.id)
                role = fguild.get_role(int(await self.bot.testdb1.fetchval("SELECT role FROM reactionroles WHERE emoji = $1 AND msg_id = $2",
                                        reaction.emoji.id,reaction.message.id)))
                await user.add_roles(role)

                em = discord.Embed(
                    title="Role Added",
                    description=f"You have got the {role.name} by reacting in {fguild.name}",
                    color=await fetch_color(bot=self.bot,ctx=await self.bot.get_context(reaction.message))
                )
                try:
                    await user.send(embed=em)
                except:
                    pass
        except:
            pass

    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction,user):
        guild_id = reaction.message.guild.id
        msg_ids = role_ids = emoji_ids = []
        msg_ids_rec = role_ids_rec = emoji_names_rec = []

        msg_ids_rec = await self.bot.testdb1.fetch("SELECT msg_id FROM reactionroles WHERE guild_id = $1",guild_id)
        msg_ids = [m['msg_id'] for m in msg_ids_rec]

        for msg_id in msg_ids:
            role_ids.append(await self.bot.testdb1.fetchval("SELECT role FROM reactionroles WHERE guild_id = $1 AND msg_id = $2",guild_id,int(msg_id)))
            emoji_ids.append(await self.bot.testdb1.fetchval("SELECT emoji FROM reactionroles WHERE guild_id = $1 AND msg_id = $2",guild_id,int(msg_id)))
        
        fguild = self.bot.get_guild(int(guild_id))

        try:
            if reaction.emoji.id in emoji_ids and reaction.message.id in msg_ids:
                rid = await self.bot.testdb1.fetchval("SELECT role FROM reactionroles WHERE emoji = $1 AND msg_id = $2"
                                                    ,reaction.emoji.id,reaction.message.id)
                role = fguild.get_role(int(await self.bot.testdb1.fetchval("SELECT role FROM reactionroles WHERE emoji = $1 AND msg_id = $2",
                                        reaction.emoji.id,reaction.message.id)))
                await user.remove_roles(role)

                em = discord.Embed(
                    title="Role Removed",
                    description=f"You have got the {role.name} removed by unreacting in {fguild.name}",
                    color=await fetch_color(bot=self.bot,ctx=await self.bot.get_context(reaction.message))
                )
                try:
                    await user.send(embed=em)
                except:
                    pass
        except:
            pass

    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()

    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS reactionroles (guild_id bigint,msg_id bigint,role bigint,emoji bigint)")
    

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
    print(Fore.GREEN+"[STATUS OK] Reactionrole cog is ready!")
