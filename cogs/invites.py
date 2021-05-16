from datetime import datetime
import asyncpg
import asyncio
import discord
from discord.ext import commands
from cogs.utils.color import fetch_color
from colorama import init,Fore
from cogs.utils.emoji import cross

init(autoreset=True)

class InviteManager(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.loop.create_task(self.setup())

    async def update_totals(self,member):
        invites = await member.guild.invites()

        c = datetime.today().strftime("%Y-%m-%d").split('-')
        c_y = int(c[0])
        c_m = int(c[1])
        c_d = int(c[2])

        async with self.bot.testdb1.execute("SELECT id,uses FROM invites WHERE guild_id = $1",member.guild.id) as cursor:
            async for invite_id, old_uses in cursor:
                for invite in invites:
                    if invite.id == invite_id and invite.uses - old_uses > 0:
                        if not (c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7):
                            await self.bot.testdb1.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = $1 AND id = $2",invite.guild.id,invite.id)
                            await self.bot.testdb1.execute("INSERT OR IGNORE INTO joined (guild_id,inviter_id,joiner_id) VALUES ($1,$2,$3)",invite.guild.id,invite.inviter.id,member.id)
                            await self.bot.testdb1.execute("UPDATES totals SET normal = normal + 1 WHERE guild_id = $1 AND inviter_id = $2",invite.guild.id,invite.inviter.id)
                        else:
                            await self.bot.testdb1.execute("UPDATE totals SET normal = normal + 1,fake = fake + 1 WHERE guild_id = $1 and inviter_id = $2",invite.guild.id,invite.inviter.id)

                        return


    @commands.Cog.listener()
    async def on_member_join(self,member):
        try:
            await self.update_totals(member)
        
            await self.invites(commands.Context,member)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        try:
            temp_res = await self.bot.testdb1.fetch("SELECT inviter_id FROM joined WHERE guild_id = $1 and joiner_id = $2",member.guild.id,member.id)
            res = [r['inviter_id'] for r in temp_res]
            if res is None:
                return
            
            inviter = res[0]

            await self.bot.testdb1.execute("DELETE FROM joined WHERE guild_id = $1 and joiner_id = $2",member.guild.id,member.id)
            await self.bot.testdb1.execute("DELETE FROM totals WHERE guild_id = $1 and inviter_id = $2",member.guild.id,member.id)
            await self.bot.testdb1.execute("UPDATE totals SET left_users = left_users + 1 WHERE guild_id = $1 and inviter_id = $2",member.guild.id,inviter)
        except:
            pass


    @commands.Cog.listener()
    async def on_invite_create(self,invite):
        try:
            await self.bot.testdb1.execute("INSERT OR IGNORE INTO totals (guild_id,inviter_id,normal,left_users,fake) VALUES ($1,$2,$3,$4,$5)",invite.guild.id,invite.inviter.id,invite.uses,0,0)
            await self.bot.testd1.execute("INSERT OR IGNORE INTO invites (guild_id,id,uses) VALUES ($1,$2,$3)",invite.guild.id,invite.id,invite.uses)
        except:
            pass

    @commands.Cog.listener()
    async def on_invite_delete(self,invite):
        try:
            await self.bot.testdb1.execute("DELETE FROM invites WHERE guild_id = $1 AND id = $2",invite.guild.id,invite.id)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        try:
            for invite in await guild.invites():
                await self.bot.testdb1.execute("INSERT OR IGNORE INTO invites (guild_id,id,uses) VALUES ($1,$2,$3)",guild.id,invite.id,invite.uses)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        try:
            await self.bot.testdb1.execute("DELETE FROM totals WHERE guild_id = $1",guild.id)
            await self.bot.testdb1.execute("DELETE FROM invites WHERE guild_id = $1",guild.id)
            await self.bot.testdb1.execute("DELETE FROM joined WHERE guild_id = $1",guild.id)
        except:
            pass

    
    @commands.command()
    @commands.bot_has_permissions(
        send_messages=True,
        manage_guild=True
    )
    async def invites(self,ctx,member:discord.Member=None):
        await self.bot.wait_until_ready()
        
        for guild in self.bot.guilds:
            try:
                for invite in await guild.invites():
                    await self.bot.testdb1.execute("INSERT OR IGNORE INTO invites (guild_id,id,uses) VALUES ($1,$2,$3)",invite.guild.id,invite.id,invite.uses)
                    await self.bot.testdb1.execute("INSERT OR IGNORE INTO totals (guild_id,inviter_id,normal,left_users,fake) VALUES ($1,$2,$3,$4,$5)",guild.id,invite.inviter.id,0,0,0)
            except:
                pass
            
            # not checking the perms here as we are going to have a error cog seperately :)

        if member is None: member = ctx.author

        cur = await self.bot.testdb1.fetch("SELECT normal,left_users,fake FROM totals WHERE guild_id = $1 and inviter_id = $2",ctx.guild.id,member.id)
        res = None
        for n,l,f in cur:
            res = n['normal'],l['left_users'],f['fake']
        
        if res is None:
            normal,left,fake = 0,0,0
        else:
            normal,left,fake = res
        
        total = normal - (left + fake)
        em = discord.Embed(
            title = f"Invites of {member.name}#{member.discriminator}",
            description = f"{member.mention} currenty has **{total}** invites.",
            timestamp = datetime.now(),
            color = await fetch_color(bot=self.bot,ctx=ctx)
        )

        await ctx.send(embed=em)

    async def setup(self):
        await self.bot.wait_until_ready()
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS switches (guild_id bigint,flag boolean, PRIMARY KEY(guild_id))")
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS totals (guild_id bigint,inviter_id bigint,normal int,left_users int,fake int, PRIMARY KEY(guild_id,inviter_id))")
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS invites (guild_id bigint,id character varying,uses int,PRIMARY KEY(guild_id,id))")
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS joined (guild_id bigint,inviter_id bigint,joiner_id bigint,PRIMARY KEY(guild_id,inviter_id,joiner_id))")

        for guild in self.bot.guilds:
            for invite in await guild.invites():
                await self.bot.testdb1.execute("INSERT OR IGNORE INTO invites (guild_id,id,uses) VALUES ($1,$2,$3)",invite.guild.id,invite.id,invite.uses)
                await self.bot.testdb1.execute("INSERT OR IGNORE INTO totals (guild_id,inviter_id,normal,left_users,fake) VALUES ($1,$2,$3,$4,$5)",guild.id,invite.inviter.id,0,0,0)



def setup(bot):
    bot.add_cog(InviteManager(bot))
    print(Fore.GREEN+"[STATUS OK] Invite cog is ready!")