import discord
from discord.ext import commands
import speedtest
import asyncio
from cogs.utils.emoji import loading, tick, cross
import os
from cogs.utils.embed_templates import basic1
from cogs.utils.color import fetch_color
from functools import lru_cache
import requests
import io
import PIL
import re
from io import BytesIO
from matplotlib import pyplot as plt
import functools

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def convert(argument):
    time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
    time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.snipe_dict = {}

    @commands.command()
    @commands.is_owner()
    async def joina(self, ctx, channel: discord.VoiceChannel):
        await channel.connect()

    @commands.command()
    @commands.is_owner()
    async def leavea(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    @commands.is_owner()
    async def speedtest(self, ctx):
        s = speedtest.Speedtest()
        msg = await ctx.send(f"{loading} Calculating your net's speed ...")
        data = os.popen("speedtest-cli --simple --share").read()
        e = discord.Embed(description=" ", color=discord.Color.orange())
        res = data.split()
        img_url = res[len(res) - 1]
        e.add_field(name="Speedtest Results - ", value=data)
        e.set_image(url=img_url)
        await msg.edit(embed=e)

    @commands.command()
    async def enlarge(self, ctx, emoji: discord.Emoji):
        ''' Enlarge any emoji '''
        # url = ctx.emoji.url_as(self,format='png')
        url = emoji.url
        await ctx.send(url)

    @commands.command(aliases=['av'])
    # @lru_cache(maxsize=None)
    async def avatar(self, ctx, *, user: discord.Member = None):
        ''' Get any user's avatar image '''
        user = user or ctx.author

        e = discord.Embed(title=f"{user.name}'s avatar", color=await fetch_color(bot=self.bot, ctx=ctx))
        e.description = f'[PNG]({user.avatar_url_as(format="png")}) | [JPEG]({user.avatar_url_as(format="jpeg")}) | [WEBP]({user.avatar_url_as(format="webp")})'
        e.set_image(url=str(user.avatar_url_as(format='png')))
        e.set_footer(text=f'Requested by {str(ctx.author)}', icon_url=ctx.author.avatar_url)

        if user.is_avatar_animated():
            e.description += f' | [GIF]({user.avatar_url_as(format="gif")})'
            e.set_image(url=str(user.avatar_url_as(format='gif')))

        return await ctx.send(embed=e)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def steal(self, ctx, *, emoji_id):
        ''' Steal any emoji by entering its id '''
        emoji = self.bot.get_emoji(int(emoji_id))
        # url = emoji.url_as(format="png")
        url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png?v=1"
        response = requests.get(url)
        b = response.content
        await ctx.guild.create_custom_emoji(name='stolen_emoji', image=b)
        await ctx.send(f"{tick} | Emoji successfully added to your server with name `stolen_emoji`")

    @commands.command()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)
        if command is None:
            await ctx.send(f"{cross} | I can't find a command with that name!")
        elif ctx.command == command:
            await ctx.send(f"{cross}| You can't disable this command")
        else:
            command.enabled = not command.enabled
            ternary = 'enabled' if command.enabled else 'disabled'
            await ctx.send(f"{tick} | Command {command.qualified_name} is {ternary}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.bot.snipe_dict[f"{message.guild.id}"] = (message.content, message.channel.name, message.author.name)

    @commands.command()
    @commands.bot_has_permissions(
        send_messages=True
    )
    async def snipe(self, ctx):
        ''' See the content of the last deleted message '''
        try:
            content, channel, author = self.bot.snipe_dict[f"{ctx.guild.id}"]
        except:
            return await ctx.send(f"{cross} | The message could not be loaded")
        if len(content) >= 2000:
            return await ctx.send(f"{cross} | Message was very big.")
        em = discord.Embed(
            description=f"Message sent by {author} in channel {channel}",
            color=await fetch_color(bot=self.bot, ctx=ctx)
        )
        em.add_field(
            name="__Message Content__",
            value=f"{content}"
        )
        em.set_footer(
            text=f"Requested by - {ctx.message.author}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(
        send_messages=True
    )
    async def reminder(self, ctx, time, *, text):
        ''' Set a reminder of any task '''
        if text is None or text == "":
            return await ctx.send(f"{cross} | Please enter valid task for reminder!")
        rem_time = convert(time)
        await ctx.send(f"{tick} | Reminder set successfully!")
        await asyncio.sleep(rem_time)
        await ctx.send(f"{ctx.author.mention} Reminder - {text}")

    async def say_permissions(self,ctx,member,channel):
        permissions = channel.permissions_for(member)
        e = discord.Embed(colour=await fetch_color(bot=self.bot,ctx=ctx))
        avatar = member.avatar_url_as(static_format='png')
        e.set_author(name=str(member), url=avatar)
        e.set_thumbnail(url=member.avatar_url)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='Allowed', value='\n'.join(allowed))
        e.add_field(name='Denied', value='\n'.join(denied))
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def permissions(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
        """Shows a member's permissions in a specific channel.
        If no channel is given then it uses the current one.
        You cannot use this in private messages. If no member is given then
        the info returned will be yours.
        """
        channel = channel or ctx.channel
        if member is None:
            member = ctx.author

        await self.say_permissions(ctx, member, channel)

    @commands.command()
    async def contact(self,ctx,*,msg):
        ''' Contact the bot owner for any query '''
        owner = self.bot.get_user(self.bot.owner_id)
        em = discord.Embed(title=f"Message from {ctx.author.name}#{ctx.author.discriminator} `[{ctx.author.id}]`",
                            description=f"```\n{msg}\n```")
        await owner.send(embed=em)
        await ctx.send(f"{tick} | Your message has been delivered to the owner of this bot!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveallhumans(self,ctx,role:discord.Role):
        ''' Gives all the humans any role '''
        humans = [mem for mem in ctx.guild.members if not mem.bot]
        for h in humans:
            await h.add_roles(role)
        await ctx.send(f"{tick} | Successfully given {role.mention} to all members!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveallbots(self,ctx,role:discord.Role):
        ''' Give all bots any role '''
        humans = [mem for mem in ctx.guild.members if mem.bot]
        for h in humans:
            await h.add_roles(role)
        await ctx.send(f"{tick} | Successfully given {role.mention} to all bots!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeallhumans(self,ctx,role:discord.Role):
        ''' Removes a role from all human members '''
        humans = [mem for mem in ctx.guild.members if not mem.bot]
        for h in humans:
            await h.remove_roles(role)
        await ctx.send(f"{tick} | Successfully removed {role.mention} from all members!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeallbots(self,ctx,role:discord.Role):
        ''' Removes a role from all the bots '''
        humans = [mem for mem in ctx.guild.members if mem.bot]
        for h in humans:
            await h.remove_roles(role)
        await ctx.send(f"{tick} | Successfully removed {role.mention} from all bots!")

    @commands.command()
    @commands.is_owner()
    async def broadcast(self,ctx,*,msg):
        rec_chnls = await self.bot.testdb1.fetch("SELECT setup_channel FROM guild_config")
        chnls = [r['setup_channel'] for r in rec_chnls if r['setup_channel'] is not None]
        for chnl in chnls:
            ch = self.bot.get_channel(int(chnl))
            await ch.send(msg)
        await ctx.send(f"{tick} | Broadcasted the messages to all the setup channels!")
    
    @commands.command()
    async def source(self, ctx):
        ''' Get the source code of the bot '''
        await ctx.send(f"Ordinate is now **private sourced**! You may request access by DMing 𝓢𝓬𝔂𝓹𝓱𝓮𝓻#9211. Dm him your __username__ and the __reason__ why you wish to view the source. Your request will then be reviewed.")

    @commands.command(aliases=['suggestion'])
    @commands.bot_has_guild_permissions(send_messages=True)
    @commands.has_guild_permissions(send_messages=True)
    async def suggest(self,ctx,*,msg):
        ''' Give some suggestions.. '''
        suggestion_channel = 821029466302054421 # PVT CHANNEL
        channel = discord.utils.get(self.bot.get_all_channels(),id=suggestion_channel)
        webhook_list = await channel.webhooks()
        webhook_names= []
        for webhook in webhook_list:
            webhook_names.append(webhook.name)
        if "Ordinate | Suggestions" not in webhook_names:
            suggestion_hook = await channel.create_webhook(name="Ordinate | Suggestions")
        else:
            elixir_server = 821027517518839809
            server = await self.bot.fetch_guild(elixir_server)
            suggestion_hook = discord.utils.get(await server.webhooks(),name="Ordinate | Suggestions")
        em = discord.Embed(description=" ",color=discord.Color.orange())
        em.add_field(name=f"Suggestion by {ctx.message.author} ({ctx.message.author.id})",value=f"```\n{msg}```")
        em.set_footer(text="To add your suggestions use `o!suggest` command!")
        await suggestion_hook.send(embed=em,avatar_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        await ctx.send(f"{tick} | Done! Your suggestion was sent to Ordinate Support Server")

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True)
    @commands.has_guild_permissions(send_messages=True)
    async def feedback(self,ctx,*,msg):
        ''' Give your feedback '''
        suggestion_channel = 821029413269143572 # PVT CHANNEL
        channel = discord.utils.get(self.bot.get_all_channels(),id=suggestion_channel)
        webhook_list = await channel.webhooks()
        webhook_names= []
        for webhook in webhook_list:
            webhook_names.append(webhook.name)
        if "Ordinate | Feedbacks" not in webhook_names:
            suggestion_hook = await channel.create_webhook(name="Ordinate | Feedbacks")
        else:
            elixir_server = 821027517518839809
            server = await self.bot.fetch_guild(elixir_server)
            suggestion_hook = discord.utils.get(await server.webhooks(),name="Ordinate | Feedbacks")
        em = discord.Embed(description=" ",color=discord.Color.orange())
        em.add_field(name=f"Suggestion by {ctx.message.author} ({ctx.message.author.id})",value=f"```\n{msg}```")
        em.set_footer(text="To add your suggestions use `o!suggest` command!")
        await suggestion_hook.send(embed=em,avatar_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        await ctx.send(f"{tick} | Done! Your suggestion was sent to Ordinate Support Server")

    

def setup(bot):
    bot.add_cog(Others(bot))
    print(OKGREEN + "[STATUS OK] Others cog is ready!")
