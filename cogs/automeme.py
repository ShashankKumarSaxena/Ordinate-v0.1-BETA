import discord
from discord.ext import commands,tasks
import requests
import sys
from cogs.utils.emoji import tick,cross
from cogs.utils.color import fetch_color
from discord import AsyncWebhookAdapter

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class AutoMeme(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # self.bot.loop.create_task(self.setup())

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_webhooks=True)
    @commands.bot_has_permissions(manage_webhooks=True)
    async def automeme(self,ctx):
        ''' Get fresh memes every 10 minutes '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    
    @automeme.command(pass_context=True)
    @commands.has_permissions(manage_webhooks=True)
    @commands.bot_has_permissions(manage_webhooks=True)
    async def enable(self,ctx,channel:discord.TextChannel=None):
        ''' Use this command to enable automeme in a channel '''

        # QUERY - 
        # CREATE TABLE public.automeme
        # (
        #     guild_id bigint,
        #     url character varying,
        #     PRIMARY KEY (guild_id)
        # );

        channel = channel or ctx.message.channel
        # await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS automeme(guild_id bigint,url character varying, PRIMARY KEY (guild_id))")
        webhook = await channel.create_webhook(name="Ordinate | Automeme")
        webhook_url = webhook.url
        url = await self.bot.testdb1.fetchval("SELECT url FROM automeme WHERE guild_id = $1",ctx.guild.id)
        if url is None:
            await self.bot.testdb1.execute("INSERT INTO automeme(guild_id,url) VALUES ($1,$2)",ctx.guild.id,webhook_url)
            await ctx.send(f"{tick} | Automeme enabled successfully for this server!")
        else:
            await self.bot.testdb1.execute("UPDATE automeme SET url = $1 WHERE guild_id = $2",webhook_url,ctx.guild.id)
            await ctx.send(f"{tick} | Updated automeme channel for this server!")


    @automeme.command()        
    @commands.bot_has_permissions(send_messages=True)
    async def disable(self,ctx):
        ''' To disable automeme in server '''
        await self.bot.testdb1.execute("DELETE FROM automeme WHERE guild_id = $1",ctx.guild.id)
        await ctx.send(f"{tick} | Automeme successfully disabled for this server!")

    @tasks.loop(minutes=10)
    async def send_meme(self):
        await self.bot.wait_until_ready()
        webhook_urls = await self.bot.testdb1.fetch("SELECT url FROM automeme")
        for rec_url in webhook_urls:
            url = rec_url["url"]
            hook = discord.Webhook.from_url(url,adapter=discord.RequestsWebhookAdapter())
            try:
                while True:
                    r = requests.get("https://memes.blademaker.tv/api")
                    data = r.json()
                    if data['nsfw'] == False:
                        break
                guild_id = await self.bot.testdb1.fetchval("SELECT guild_id FROM automeme WHERE url = $1",str(url))
                color = await self.bot.testdb1.fetchval("SELECT color FROM colors WHERE guild_id = $1",guild_id)
                if color is None:
                    color = discord.Color.orange()
                else:
                    color = color
                em = discord.Embed(title=f"{data['title']}",color=color)
                em.set_image(url=data['image'])
                em.set_footer(text=f"Ups - {data['ups']} Downs - {data['downs']}")
                await hook.send(embed=em,avatar_url="https://cdn.discordapp.com/avatars/798557068998738000/d42b7eac0a9d8d804112a04b82a95964.png?size=1024")
            except Exception as e:
                pass

    
    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS automeme(guild_id bigint,url character varying, PRIMARY KEY (guild_id))")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()
        self.send_meme.start()



def setup(bot):
    bot.add_cog(AutoMeme(bot))
    print(OKGREEN + "[STATUS OK] Automeme cog is ready!")


