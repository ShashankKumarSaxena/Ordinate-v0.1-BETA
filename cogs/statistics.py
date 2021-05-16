import discord
from discord.ext import commands
import time 
import datetime
from cogs.utils.emoji import online,dnd,offline,idle,cross
from hurry.filesize import size
import psutil
from disputils import BotEmbedPaginator
import math
from cogs.utils.lister import lister

# PSUTILS
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Stats(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    async def fetch_color(self,ctx):
        color = await self.bot.testdb1.fetchval("SELECT color FROM colors WHERE guild_id = $1",ctx.guild.id)
        if not color:
            return discord.Color.orange()
        else:
            return int(color)

    #================ REWRITE HERE ================#

    @commands.command(aliases=["uinfo"])
    @commands.bot_has_permissions(send_messages=True)
    async def userinfo(self,ctx,*,user:discord.Member=None):
        ''' Get the user information with this command '''
        # TODO - Correct the activity for Bots
        if user is None:
            user = ctx.message.author
        if user not in ctx.guild.members:
            await ctx.send(f"{cross} Sorry no user named {user} found in this server.")
        # em = discord.Embed(title="User Information",color=discord.Color.orange())
        color = await self.fetch_color(ctx)
        em = discord.Embed(title="User Information",color=color)
         # KUNDLI HERE
        em.add_field(name="__General Information__",value=f"**Name :** {user.name}\n"
                                                f"**Nickname :** {user.nick}\n"
                                                f"**ID :** {user.id}\n"
                                                f"**Discriminator :** {user.discriminator}\n"
                                                f"**Joined discord at :** {user.created_at}\n"
                                                f"**Avatar URL :** [Download Here]({user.avatar_url})\n"
                                                f"**Is bot? :** {user.bot}",inline=False)
        is_boosting = True if user.premium_since else False
        em.add_field(name="__Server Information__",value=f"**Joined at :** {user.joined_at}\n"
                                                f"**Is boosting? :** {is_boosting}\n"
                                                f"**Top role :** {user.top_role.mention}",inline=False) 

        stat = ""
        rstat = ""
        if "online" in user.status:
            stat = online
            rstat = "Online"
        elif "idle" in user.status:
            stat = idle
            rstat = "Idle"
        elif "dnd" or "do_not_disturb" in user.status:
            stat = dnd
            rstat = "Do not disturb"
        elif "offline" in user.status:
            stat = offline
            rstat = "Offline"
        elif "invisible" in user.status:
            stat = offline
            rstat = "Invisible"
        em.add_field(name="__Activites__",value=f"**Status :** {stat} | {rstat}\n"
                                                f"**Activity :** {user.activity}",inline=False)                    

        em.add_field(name="__Roles__",value=f" ".join(f"{role.mention}" for role in list(user.roles)),inline=False)

        em.set_thumbnail(url=user.avatar_url)
        em.set_footer(text=f"Requested By : {ctx.message.author}")

        await ctx.send(embed=em)
            # ANY ERROR???


        #===============================================#
    
    @commands.command(aliases=['cinfo'])
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    # @commands.has_permissions(kick_members=True)
    async def channelinfo(self,ctx):
        ''' Get the channels information '''
        channel = ctx.channel
        tmembers = str(len(channel.members))
        nsfw = ctx.channel.is_nsfw()
        news = ctx.channel.is_news()
        color = await self.fetch_color(ctx)
        embed = discord.Embed(title=f"{ctx.channel}",color=color)
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="__Channel Information__",value=
                                                f"**Channel Name: ** {channel.name}\n"
                                                f"**Channel ID: ** {channel.id}\n"
                                                f"**Channel type: ** {channel.type}\n"
                                                f"**Channel category: ** {channel.category}\n"
                                                f"**Topic: ** {channel.topic}\n"
                                                f"**Channel position: ** {channel.position}\n"
                                                f"**Created at: ** {channel.created_at.strftime('%a,%#d %B %Y, %I:%M %p ')}\n"
                                                f"**Slowmode: ** {channel.slowmode_delay}\n"
                                                f"**Channel Permissions: ** {channel.permissions_synced}\n"
                                                f"**Channel members: ** {tmembers}\n"
                                                f"**Is nsfw: ** {nsfw}\n"
                                                f"**Is news: ** {news}",inline=False)

        embed.set_author(name="Ordinate Bot",icon_url=f"{ctx.me.avatar_url}")
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases=["rinfo"]) # hidden=True
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    # @commands.has_permissions(kick_members=True)
    async def roleinfo(self,ctx,*,rolename):
        ''' Get role information with this command '''
        allowed = []
        try:
            role = discord.utils.get(ctx.message.guild.roles,name=rolename)
            permissions = role.permissions
            for name,value in permissions: 
                if value:
                    name = name.replace('_',' ').replace('guild','server').title()
                    allowed.append(name)
        except:
            return await ctx.send(f"Could not find the role **{rolename}**")
        time = role.created_at
        color = await self.fetch_color(ctx)
        em = discord.Embed(description=f"",color=color,timestamp=time)
        em.set_author(name=f"{rolename}")
        # em.set_author(name=f"{role.mention}")
        em.set_thumbnail(url=f"{ctx.guild.icon_url}")
        em.add_field(name="__Information__",value=f"Role : {role.mention}\n"
                                                f"**ID :** {str(role.id)}\n"
                                                f"**Color : {role.color}\n"
                                                f"**Position : {str(role.position)}\n"
                                                f"**Hoisted : ** {str(role.hoist)}\n"
                                                f"**Is mentionable :** {str(role.mentionable)}\n"
                                                f"**Members in role :** {str(len(role.members))}\n")
        em.add_field(name="__Role Permissions__",value=f", ".join(allowed), inline=False)
        em.set_footer(text=f"Requested by - {ctx.message.author}")
        # await ctx.send(f"{role.mention}")
        await ctx.send(embed=em)

    # emoji lister to be made

    @commands.command(aliases=["sinfo"])
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    # @commands.has_permissions(kick_members=True)
    async def serverinfo(self,ctx):
        ''' Get server information with this command '''
        afk_channel = ctx.guild.afk_channel
        banner = ctx.guild.banner
        banner_url = ctx.guild.banner_url
        no_of_categories = len(ctx.guild.categories)
        no_of_channels = len(ctx.guild.channels)
        created_at = ctx.guild.created_at
        default_role = ctx.guild.default_role
        guild_description = ctx.guild.description
        filesize_limit = ctx.guild.filesize_limit
        icon = ctx.guild.icon
        icon_url = ctx.guild.icon_url
        ID = str(ctx.guild.id)
        max_members = ctx.guild.max_members
        who_are_you = ctx.guild.me
        owner = ctx.guild.owner
        owner_id = ctx.guild.owner_id
        # prem_subs_role = ctx.guild.premium_subscriber_role
        premium_subscribers = ctx.guild.premium_subscribers
        premium_subscribers_no = ctx.guild.premium_subscription_count
        region = ctx.guild.region
        role_list = ctx.guild.roles
        no_of_roles = len(ctx.guild.roles)
        # your_roles= ctx.guild.self_role
        no_of_text_channels = len(ctx.guild.text_channels)
        no_of_voice_channels = len(ctx.guild.voice_channels)
        # if prem_subs_role is None:
        #     prem_subs_role = 0

        # em = discord.Embed(description=f"",color=discord.Color.orange())
        # em.set_author(name=f"{ctx.guild.name}")
        # em.set_thumbnail(url=f"{ctx.guild.icon_url}")
        # em.add_field(name="__Server Information__",value=f"ID : {ID}\n"
        #                                                 f"No. of channels : {no_of_channels}\n"
        #                                                 f"No. of categories : {no_of_categories}\n"
        #                                                 f"No. of roles : {no_of_roles}\n"
        #                                                 f"Created at : {created_at}\n"
        #                                                 f"Owner : {owner}\n"
        #                                                 f"Owner ID : {owner_id}\n"
        #                                                 f"Icon URL : [Download Here]({icon_url})\n"
        #                                                 f"Banner URL : [Download Here]({banner_url})\n"
        #                                                 f"Filesize Limit : {filesize_limit}\n"
        #                                                 f"Maximum Members : {max_members}\n"
        #                                                 f"Premium Subscriber's role : {prem_subs_role}\n"
        #                                                 f"No. of premium subscribers : {premium_subscribers_no}\n"
        #                                                 f"Region : {str(region).upper()}\n"
        #                                                 f"No. of text channels : {no_of_text_channels}\n"
        #                                                 f"No. of voice channels : {no_of_voice_channels}\n"
        #                                                 f"AFK Channel : {afk_channel}\n"
        #                                                 f"Rules Channel : {ctx.guild.rules_channel}\n"
        #                                                 f"Who are you? : {ctx.message.author}",inline=False)
        # em.add_field(name="__Description__",value=f"{guild_description}",inline=False)

        color = await self.fetch_color(ctx)

        em = discord.Embed(title="__Server Information__",color=color)
        em.add_field(name="__General Info__",value=f"**Server's Name :** {ctx.guild.name}\n"
                                            f"**Server's ID :** {ctx.guild.id}\n"
                                            f"**Region :** {str(ctx.guild.region).upper()}\n"
                                            f"**Created At :** {ctx.guild.created_at}\n"
                                            f"**Icon URL :** [Download Here]({ctx.guild.icon_url})\n"
                                            f"**Banner URL :** [Download Here]({ctx.guild.banner_url})\n",inline=False)
        st = ""
        if "online" in ctx.guild.owner.status:
            st = online
        elif "offline" in ctx.guild.owner.status or "invisible" in ctx.guild.owner.status:
            st = offline
        elif "idle" in ctx.guild.owner.status:
            st = idle
        elif "dnd" in ctx.guild.owner.status or "do_not_disturb" in ctx.guild.owner.status:
            st = dnd
            
        em.add_field(name="__Owner's Info__",value=f"**Owner's name :** {ctx.guild.owner}\n"
                                                f"**Owner's ID :** {ctx.guild.owner.id}\n"
                                                f"**Nickname :** {ctx.guild.owner.nick}\n"
                                                f"**Owner's status :** {st}\n"
                                                f"**Activity :** {ctx.guild.owner.activity}\n"
                                                ,inline=True)

        em.add_field(name="__Channel Info__",value=f"**Total channels :** {len(ctx.guild.channels)}\n"
                                                f"**Text channels :** {len(ctx.guild.text_channels)}\n"
                                                f"**Voice channels :** {len(ctx.guild.voice_channels)}",inline=True)

        # em.add_field(name="‎",value="‎‎ ",inline =True)

        # em.add_field(name="á̭̟̙̤̞͋̇̔̊̉͂͆͑͒̽͐b̳̥̮͍͍͍̭͉̮̟͍̉̑̅͋̽̄̍c͙͇̟͚̣̘̘͍̔̂̓̒̿̅̈̽",value="á̭̟̙̤̞͋̇̔̊̉͂͆͑͒̽͐b̳̥̮͍͍͍̭͉̮̟͍̉̑̅͋̽̄̍c͙͇̟͚̣̘̘͍̔̂̓̒̿̅̈̽",inline =True)


        online_memb = []
        offline_memb = []
        idle_memb = []
        dnd_memb = []
        bot_count = 0
        for member in ctx.guild.members:
            if member.bot == True:
                bot_count += 1
            if "online" in member.status:
                online_memb.append(online)
            elif "offline" in member.status or "invisible" in member.status:
                offline_memb.append(offline)
            elif "idle" in ctx.guild.owner.status:
                idle_memb.append(idle)
            elif "dnd" in member.status or "do_not_disturb" in member.status:
                dnd_memb.append(dnd)

        em.add_field(name="__Members__",value=f"**Total members :** {len(ctx.guild.members)}\n"
                                            f"**Bots :** {bot_count}\n"
                                            f"{online}{len(online_memb)} {dnd}{len(dnd_memb)} {idle}{len(idle_memb)} {offline}{len(offline_memb)}\n"
                                            f"**Premium Subscribers :** {premium_subscribers_no}",inline =False)

        # em.add_field(name="‎",value="‎‎ ",inline =True)

        em.add_field(name="__Other__",value=f"**Maximum members allowed :** {ctx.guild.max_members}\n"
                                            f"**Categories : ** {len(ctx.guild.categories)}\n"
                                            f"**Filesize limit :** {size(ctx.guild.filesize_limit)}\n"
                                            f"**Who are you? :** {ctx.message.author}",inline=True)

        animated = 0
        for emoji in ctx.guild.emojis:
            if emoji.animated:
                animated += 1
        em.add_field(name="__Emoji__",value=f"**Total emojis :** {len(ctx.guild.emojis)}\n"
                                            f"**Animated : ** {animated}\n"
                                            f"**Allowed : **{ctx.guild.emoji_limit}",inline=True)

        # em.add_field(name="‎",value="‎‎ ",inline =True)

        em.set_thumbnail(url=ctx.guild.icon_url)

        if no_of_roles < 40:
            em.add_field(name="__Roles__",value=f" ".join(f"{role.mention}" for role in role_list),inline=False)
        else:
            role_list = role_list[0:24]
            em.add_field(name="__Roles__",value=f" ".join(f"{role.mention}" for role in role_list),inline=False)

        em.set_footer(text=f"Requested by - {ctx.message.author}")
        await ctx.send(embed=em)

        
    
    @commands.command(aliases=["catinfo"])
    @commands.bot_has_permissions(send_messages=True)
    async def categoryinfo(self,ctx,category:discord.CategoryChannel=None):
        ''' Get information about a category'''
        if category is None:
            category = ctx.channel.category
        ID = category.id
        name = category.name
        text_channels = len(category.text_channels)
        voice_channels = len(category.voice_channels)
        total_channels = len(category.channels)
        created_at = category.created_at
        color = await self.fetch_color(ctx)
        em = discord.Embed(description=f"__Category Information__",color=color)
        em.add_field(name=f"About category : {category}",value=f"ID : {ID}\n"
                                                    f"Name : {name}\n"
                                                    f"Total Channels : {total_channels}\n"
                                                    f"Text Channels : {text_channels}\n"
                                                    f"Voice Channels : {voice_channels}\n"
                                                    f"Created At : {created_at}\n")
        em.set_thumbnail(url=ctx.guild.icon_url)
        # em.set_image(url=ctx.messaavatar_url)
        em.set_footer(text=f"Requested By : {ctx.message.author}")
        await ctx.send(embed=em)

    # @commands.command(aliases=["stats"])
    # @commands.bot_has_permissions(send_messages=True)
    # async def botstats(self,ctx):
    #     bot_version = "v1.0.2 [BETA]"
    #     owner_id = self.bot.owner_id
    #     owner_name = "𝓢𝓱𝓪𝓼𝓱𝓪𝓷𝓴𝓚𝓾𝓶𝓪𝓻27#9211"
    #     no_of_guilds = len(self.bot.guilds)
    #     no_of_users = len(self.bot.users)
    #     python_version = "3.8.3"
    #     em = discord.Embed(description="Bot Stats",color=discord.Color.orange())
    #     em.add_field(name="General",value=f"Bot Version : `{bot_version}`\n"
    #                                     f"Python Version : `{python_version}`\n"
    #                                     f"Owner & Developer : `{owner_name}`\n",inline=False)
    #     em.add_field(name="Fame",value=f"Guilds : `{no_of_guilds}`\n"
    #                                     f"Users : `{no_of_users}`\n",inline=False)
    #     em.set_footer(text=f"Requested By : {ctx.message.author}")
    #     await ctx.send(embed=em)

    #============= REWRITE HERE ===============##

    @commands.command(aliases=["stats","info"])
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def botinfo(self,ctx):
        ''' Get information about this bot '''
        now = datetime.datetime.utcnow()
        elapsed = now - self.bot.starttime
        seconds = elapsed.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)   
        cpu = str(psutil.cpu_percent())
        
        color = await self.fetch_color(ctx)

        em = discord.Embed(description=" ",color=color)
        em.add_field(name="Bot Stats",value=f"```asciidoc\nName:: {ctx.guild.me} [{ctx.guild.me.id}]\n"
                                            +f"Bot latency:: {round(self.bot.latency * 1000)}ms\n"
                                            +f"Uptime:: {elapsed.days} days, {hours} hours, {minutes} minutes and {seconds} seconds\n```",inline=False)
        users = 0
        for guild in self.bot.guilds:
            try:
                users += guild.member_count
            except:
                pass

        channels = 0
        for channel in self.bot.get_all_channels():
            channels +=1

        em.add_field(name="General",value=f"```asciidoc\n"
                                        +f"Guilds:: {len(self.bot.guilds)}\n"
                                        +f"Users:: {users}\n"
                                        +f"Channels:: {channels}\n```",inline=True)

        em.add_field(name="Bot",value=f"```asciidoc\n"
                                    +f"Python:: 3.8.3\n"
                                    +f"discord.py:: {discord.__version__}\n"
                                    +f"Bot:: {self.bot.VERSION}```",inline=True)

        em.add_field(name="System",value=f"```asciidoc\n"
                                        +f"Total Memory:: 1024Gb\n"
                                        +f"Usage:: 642Mb\n"
                                        +f"CPU Usage:: {psutil.cpu_percent()}%```",inline=True)

        owner = self.bot.get_user(766553763569336340)

        em.add_field(name="Owner",value=f"```asciidoc\n"
                                        +f"Owner:: {owner.name}#{owner.discriminator} [{owner.id}]\n```",inline=False)

        em.add_field(name="Links",value=f"[Invite]({self.bot.INVITE}) | [Support Server]({self.bot.SUPPORT_SERVER})",inline=False)

        em.set_author(name=f"About {ctx.guild.me}",icon_url=f"{ctx.guild.me.avatar_url}")

        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=em)

    #=========================================#
        
    @commands.command(aliases=('lemoji','emojis','listemoji','emojilist'))
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def listemojis(self,ctx):
        ''' Lists emojis in the server '''
        emoji_name = []
        emoji_ment = []
        emoji_list = []
        for emoji in ctx.guild.emojis:
            emoji_list.append(emoji)
            emoji_name.append(str(emoji.name))
            if emoji.animated:
                emoji_ment.append(f"`<a:{emoji.name}:{emoji.id}>`")
            else:
                emoji_ment.append(f"`<:{emoji.name}:{emoji.id}>`")
        
        pages = math.ceil(len(emoji_name)/12)
        page = [i for i in range(1,pages+1)]
        counts = []
        first_num = 0
        for i in page:
            if first_num == 0:
                last_num = (i*12) -1
            else:
                last_num = (i*12) -1
            if first_num > len(emoji_list):
                first_num = len(emoji_list)
            elif last_num > len(emoji_list):
                last_num = len(emoji_list)
            l = [first_num,last_num]
            counts.append(l)
            if last_num == len(emoji_list) or first_num == len(emoji_list):
                break
            first_num = last_num + 1
                    
        embeds = []
        color = await self.fetch_color(ctx)
        for l in counts:
            first_num = l[0]
            last_num = l[1]
            em = discord.Embed(description=" ",color=color).add_field(name=f"List of emojis in this server - [{len(emoji_name)}]",value="\n".join(f"`[{count+1}]` {emoji_list[count]} | {emoji_ment[count]}" for count in range(first_num,last_num)))
            embeds.append(em)
                
        paginator = BotEmbedPaginator(ctx,embeds)
        await paginator.run()

    @commands.command(aliases=('roles','lroles','listrole','serverroles','rolelist','roleslist'))
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def listroles(self,ctx):
        ''' Gives the list of roles in this server '''
        role_list = ctx.guild.roles
        pages = math.ceil(len(role_list)/15)
        page = [i for i in range(1,pages+1)]
        counts = []
        first_num = 0
        for i in page:
            if first_num == 0:
                last_num = (i*15) -1
            else:
                last_num = (i*15) -1
            if first_num > len(role_list):
                first_num = len(role_list)
            elif last_num > len(role_list):
                last_num = len(role_list)
            l = [first_num,last_num]
            counts.append(l)
            if last_num == len(role_list) or first_num == len(role_list):
                break
            first_num = last_num + 1
                    
        embeds = []
        color = await self.fetch_color(ctx)
        for l in counts:
            first_num = l[0]
            last_num = l[1]
            em = discord.Embed(description=" ",color=color).add_field(name=f"List of roles in this server - [{len(role_list)}]",value="\n".join(f"`[{count+1}]` {ctx.guild.roles[count].mention}" for count in range(first_num,last_num)))
            embeds.append(em)
                
        paginator = BotEmbedPaginator(ctx,embeds)
        await paginator.run()

    @commands.command()
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def vclist(self,ctx):
        ''' Get the list of members in vc you are connected to'''
        if not ctx.message.author.voice:
            await ctx.send(f"{cross} | You are not connected to any voice channels")
        else:
            member_list = ctx.message.author.voice.channel.members
            color = await self.fetch_color(ctx)
            await lister(ctx,your_list=member_list,color=color,title=f"List of members in {ctx.message.author.voice.channel.name}")

    @commands.command(aliases=('listbots','lbots','lbot','botlist','botslist'))
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def bots(self,ctx):
        ''' Lists the bots in your server '''
        bots_list = []
        for m in ctx.guild.members:
            if m.bot:
                bots_list.append(m)
        color = await self.fetch_color(ctx)
        await lister(ctx,your_list=bots_list,color=color,title=f"List of bots in {ctx.guild.name}")

    
    @commands.command(aliases=('listadmins','adminlist'))
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def admins(self,ctx):
        ''' Lists the admins of this server '''
        admin_list = []
        for m in ctx.guild.members:
            if m.guild_permissions.administrator:
                if not m.bot:
                    admin_list.append(m)
        color = await self.fetch_color(ctx)
        await lister(ctx,your_list=admin_list,color=color,title=f"List of admins in {ctx.guild.name}")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def botemojis(self,ctx):
        ''' List the emojis which this bot can see '''
        emoji_name = []
        emoji_ment = []
        emoji_list = []
        for emoji in self.bot.emojis:
            emoji_list.append(emoji)
            emoji_name.append(str(emoji.name))
            if emoji.animated:
                emoji_ment.append(f"`<a:{emoji.name}:{emoji.id}>`")
            else:
                emoji_ment.append(f"`<:{emoji.name}:{emoji.id}>`")
        
        pages = math.ceil(len(emoji_name)/15)
        page = [i for i in range(1,pages+1)]
        counts = []
        first_num = 0
        for i in page:
            if first_num == 0:
                last_num = (i*15) -1
            else:
                last_num = (i*15) -1
            if first_num > len(emoji_list):
                first_num = len(emoji_list)
            elif last_num > len(emoji_list):
                last_num = len(emoji_list)
            l = [first_num,last_num]
            counts.append(l)
            if last_num == len(emoji_list) or first_num == len(emoji_list):
                break
            first_num = last_num + 1
                    
        embeds = []
        color = await self.fetch_color(ctx)
        for l in counts:
            first_num = l[0]
            last_num = l[1]
            em = discord.Embed(description=" ",color=color).add_field(name=f"List of emojis that bot can see - [{len(emoji_name)}]",value="\n".join(f"`[{count+1}]` {emoji_list[count]} | {emoji_ment[count]}" for count in range(first_num,last_num)))
            embeds.append(em)
                
        paginator = BotEmbedPaginator(ctx,embeds)
        await paginator.run()



def setup(bot):
    bot.add_cog(Stats(bot))
    print(OKGREEN + "[STATUS OK] Stats cog is ready!")

