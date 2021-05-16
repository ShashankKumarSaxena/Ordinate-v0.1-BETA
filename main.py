import discord
from discord.ext import commands
import json
import asyncio
import sys
import os
import traceback
import jishaku
from cogs.utils.emoji import tick,cross,error_em
import ssl
# import redbot
import asyncpg
# from pretty_help import PrettyHelp
import traceback
import datetime
from cogs.utils.cache import cache
from discord_slash import SlashCommand,SlashContext
import contextlib
import logging
from logging.handlers import RotatingFileHandler
from cogs.utils.progressbar import progressBar,printProgressBar
from cogs.automeme import AutoMeme
import config

intents = discord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('>>'),case_insensitive=True,intents=intents,chunk_guilds_at_startup=False) # Should get changed to custom prefixes

slash = SlashCommand(bot,sync_commands=True)
bot.name = "Ordinate"
bot.starttime = datetime.datetime.now()
bot.VERSION = "v0.1.1t"
bot.INVITE = "https://discord.com/api/oauth2/authorize?client_id=810137345789263913&permissions=8&scope=bot%20applications.commands"
bot.SUPPORT_SERVER = "https://discord.gg/8Rfx5xw7Qe"
bot.SUPPORT_SERVER_ID = 821027517518839809 #change


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

with open("./config.json",'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData['DISCORD_TOKEN']

#================ LOGGING ===============#

class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name='discord.state')
    def filter(self,record):
        if record.levelname == "WARNING" and 'referencing an unknown' in record.msg:
            return False
        return True

@contextlib.contextmanager
def setup_logging():
    try:
        max_bytes = 32*1024*1024
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        logging.getLogger('discord.state').addFilter(RemoveNoise())

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = RotatingFileHandler(filename='thecoderzbot.log',encoding='utf-8',mode='w',maxBytes=max_bytes,backupCount=5)
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}',dt_fmt,style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)
        yield
    finally:
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


#=======================================#

@bot.event
async def on_ready():
    ''' When bot gets online '''
    
    for guild in bot.guilds:
        try:
            await bot.testdb1.execute("INSERT INTO guild_config (guild_id, welcomer, leaver, leveller,level_up_msg,nqnf,mod_logs,server_updates) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
                                        guild.id, False, False, False, True, False, False, False)
        except Exception as e:
            pass

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="o!help | o!setup"),status=discord.Status.dnd)
    print("========================================================")
    print(OKCYAN+"[DONE] The bot is online!")
    print(f"Logged in as : {bot.user.name}")
    print(f"Current Servers : {len(bot.guilds)}")
    print(f"Current Users : {len(bot.users)}")
    print("========================================================")

    #============ Auto tasks ========#

    #================================#

#========== ping commands==========#

@bot.command()
async def ping(ctx):
    await ctx.reply(f"Pong, Latency is {round(bot.latency * 1000)}ms")

guild_ids = []
for guild in bot.guilds:
    guild_ids.append(guild.id)


@slash.slash(name="ping",guild_ids=guild_ids,description="Check the latency of bot")
async def _ping(ctx):
    await ctx.respond()
    await ctx.send(content=f"Pong, latency is {round(bot.latency*1000)}ms")



#============= COGS ===========#
extensions = [
            'cogs.message',
            'cogs.moderation',
            'cogs.lockdown',
            'cogs.setup',
            'cogs.create',
            'cogs.category',
            'cogs.statistics',
            'cogs.debug',
            'cogs.role',
            'cogs.others',
            'cogs.test', #---> Only for testing purposes
            'cogs.automeme',
            'cogs.embeds',
            'cogs.status',
            'cogs.api',
            'cogs.dbhelper', # TO BE COMPLETED
            'cogs.images',
            'cogs.giveaway',
            # 'cogs.invites', #---> MALFUNCTIONING
            'cogs.todo',
            'cogs.afk',
            'cogs.reactionroles',
            'cogs.nqn', # TODO - Rewrite and understand
            'cogs.levelling',
            'cogs.events',
            'cogs.fun',
            'cogs.ticket',
            'cogs.isupport',
            'cogs.logs',
            # 'cogs.errors',
            'cogs.help',
            #'cogs.chatbot'
            
]


me = bot.get_user(766553763569336340) # LOL I can use bot.owner too


if __name__ == "__main__":
    for extension in extensions:
    # for extension in progressBar(extensions,prefix="Loading: ",suffix="Completed!",length=50):
        try:
            bot.load_extension(extension)
        except:
            print(FAIL+f"[CRITICAL] Error loading {extension}!",file=sys.stderr)
            tr = traceback.format_exc()
            bot.tr = tr

            # traceback.print_exc() #---> Remove this later or maybe dont
    loop = asyncio.get_event_loop()
    log = logging.getLogger()

try:
    bot.load_extension("jishaku")
    print(OKGREEN + "[STATUS OK] Jishaku cog is ready!")
except:
    print("Jishaku failed to load")

async def create_db_pool():
    client = ssl.create_default_context(cafile="")
    client.check_hostname = False
    client.verify_mode = ssl.CERT_NONE

    #========== Database for testing ==================#
    bot.testdb1 = await asyncpg.create_pool(config.DATABASE_URI)

    #===================================================#

    #=========== Main databases =================#

    #============================================#

    print("========================================================")
    print(OKBLUE + "[Database] Database loaded successfully!")
    # print("========================================================")

    #============ Query execution ===============#
    
    QUERIES = open('database/guildconfig.sql','r').read()
    await bot.testdb1.execute(QUERIES)

    # something missing from here

    #============================================#

    # print("========================================================")
    print(OKBLUE + "[Database] Queries executed successfully!")
    print("========================================================")

    await cache(bot)

bot.loop.create_task(create_db_pool())

try:
    with setup_logging():
        bot.run(TOKEN)
except:
    print(FAIL + "--------------> Killed!! <---------------")
finally:
    print(FAIL + "--------------> Killed!! <---------------")