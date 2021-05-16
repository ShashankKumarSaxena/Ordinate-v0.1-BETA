import discord
from discord.ext import commands
from colorama import Fore,init
from cogs.utils.color import fetch_color
from cogs.utils.emoji import cross,tick

init(autoreset=True)

class InteractiveSupport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def isupport(self,ctx,*,reason:str):
        ''' Need some help regarding bot? Use this command to open an interactive session with our staff and clear your doubts '''
        support_channel = await ctx.guild.create_text_channel(f"{ctx.author.name}-isupport")
        for category in self.bot.get_guild(self.bot.SUPPORT_SERVER_ID).categories:
            if category.name.lower() == "support":
                sserver_cate = category
                break
        sserver_channel = await sserver_cate.create_text_channel(f"{ctx.author.name}-support")
        support_hook = await support_channel.create_webhook(name="Ordinate | Support")
        sserver_hook = await sserver_channel.create_webhook(name="Ordinate | Support")

        await self.bot.testdb1.execute("INSERT INTO isupportdata (guild_id,support_channel,sserver_channel,support_url,server_url,issuer) VALUES ($1,$2,$3,$4,$5,$6)",
                                                            ctx.guild.id,support_channel.id,sserver_channel.id,support_hook.url,sserver_hook.url,f"{ctx.author.name}#{ctx.author.discriminator}")

        em1 = discord.Embed(
            title="Interactive Bot Support",
            description="Please wait, our staff will be with you shortly.",
            color=await fetch_color(bot=self.bot,ctx=ctx)
        )
        await support_channel.send(embed=em1)
        
        em2 = discord.Embed(
            title=f"Interactive Bot Support",
            description=f"{ctx.author.name}#{ctx.author.discriminator} needs some help. ID - `{ctx.author.id}`",
            color=await fetch_color(bot=self.bot,ctx=ctx)
        )

        em2.add_field(name="Reason",value=f"{reason}")
        em2.add_field(name="Guild ID",value=f"{ctx.guild.id}")

        await support_channel.set_permissions(ctx.guild.get_role(ctx.guild.id),
                                                send_messages=False,read_messages=False)

        await support_channel.set_permissions(ctx.author,send_messages=True,read_messages=True,embed_links=True,attach_files=True,read_message_history=True)

        await sserver_channel.set_permissions(self.bot.get_guild(self.bot.SUPPORT_SERVER_ID).get_role(self.bot.SUPPORT_SERVER_ID),
                                                send_messages=False,read_messages=False)


        await sserver_channel.send(embed=em2)

        em3 = discord.Embed(
            title="Interactive Bot Support",
            description=f"Your support channel has been created at {support_channel.mention}",
            color=await fetch_color(bot=self.bot,ctx=ctx)
        )
        await ctx.send(embed=em3)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        support_channel = self.bot.get_channel(await self.bot.testdb1.fetchval("SELECT support_channel FROM isupportdata WHERE guild_id = $1",message.guild.id))
        sserver_channel = self.bot.get_channel(await self.bot.testdb1.fetchval("SELECT sserver_channel FROM isupportdata WHERE guild_id = $1",message.guild.id))

        support_url = await self.bot.testdb1.fetchval("SELECT support_url FROM isupportdata WHERE guild_id = $1",message.guild.id)
        server_url = await self.bot.testdb1.fetchval("SELECT server_url FROM isupportdata WHERE guild_id = $1",message.guild.id)

        rec_user_name = await self.bot.testdb1.fetch("SELECT issuer FROM isupportdata WHERE guild_id = $1",message.guild.id)
        user_name = [r['issuer'] for r in rec_user_name]

        if message.channel == sserver_channel and message.author.name != "Ordinate | Support Staff#0000" and message.clean_content != "":
            try:
                support_hook = discord.Webhook.from_url(support_url, adapter=discord.RequestsWebhookAdapter())
                await support_hook.send(content=message.content, username=f"Ordinate | Support Staff",avatar_url="https://cdn.discordapp.com/avatars/821420835624845323/caf2962e47ff263950f14386f6bd64b0.png?size=1024")
            except TypeError:
                pass

        elif message.channel == support_channel and message.author.name != "Ordinate | Support Staff":
            if message.author == self.bot.user:
                pass
            else:
                try:
                    sserver_hook = discord.Webhook.from_url(server_url, adapter=discord.RequestsWebhookAdapter())
                    await sserver_hook.send(content=message.clean_content, username=f"{message.author.name}#{message.author.discriminator}",avatar_url=message.author.avatar_url)
                except TypeError:
                    pass
        

    @commands.command()
    async def isolved(self,ctx):
        ''' If your doubt is solved then use this command to close the session. '''
        rec_user_name = await self.bot.testdb1.fetch("SELECT issuer FROM isupportdata WHERE guild_id = $1",ctx.guild.id)
        user_name = [r['issuer'] for r in rec_user_name]

        if f"{ctx.author.name}#{ctx.author.discriminator}" in user_name:

            support_channel = self.bot.get_channel(await self.bot.testdb1.fetchval("SELECT support_channel FROM isupportdata WHERE guild_id = $1 AND issuer = $2",
                                                                                            ctx.guild.id, f"{ctx.author.name}#{ctx.author.discriminator}"))

            sserver_channel = self.bot.get_channel(await self.bot.testdb1.fetchval("SELECT sserver_channel FROM isupportdata WHERE guild_id = $1 AND issuer = $2",
                                                                                            ctx.guild.id, f"{ctx.author.name}#{ctx.author.discriminator}"))

            await support_channel.delete(reason="Bot support channel")
            await sserver_channel.delete(reason="Bot support channel")

            await self.bot.testdb1.execute("DELETE FROM isupportdata WHERE guild_id = $1 AND issuer = $2",ctx.guild.id,f"{ctx.author.name}#{ctx.author.discriminator}")

            em = discord.Embed(
                title="Interactive Bot Support",
                description=f"Thanks for contacting, we hope you got all your issues solved.",
                color=await fetch_color(bot=self.bot,ctx=ctx)
            )
            await ctx.send(embed=em)
        
        else:
            return await ctx.send(f"{cross} | You don't have any issues yet.")

    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS isupportdata (guild_id bigint, support_channel bigint, sserver_channel bigint, support_url character varying, server_url character varying, issuer character varying)")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()


def setup(bot):
    bot.add_cog(InteractiveSupport(bot))
    print(Fore.GREEN+"[STATUS OK] ISupport cog is ready!")
