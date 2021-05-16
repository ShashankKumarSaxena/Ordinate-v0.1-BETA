import discord
from discord.ext import commands
from colorama import init,Fore
from cogs.utils.api_fetcher import fetch_json,bytes_image,bytes_gif,bytes_image2
from cogs.utils.embed_templates import basic_image1,basic_image2
from cogs.utils.emoji import cross
import requests
from PIL import Image
import io
import sys

init(autoreset=True)

class Images(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases=['dogimage'])
    @commands.bot_has_permissions(send_messages=True)
    async def dog(self,ctx):
        '''
        Get random dog images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/dog")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))

    @commands.command(aliases=['catimage'])
    @commands.bot_has_permissions(send_messages=True)
    async def cat(self,ctx):
        '''
        Get random cat images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/cat")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))
    
    @commands.command(aliases=['pandaimage'])
    @commands.bot_has_permissions(send_messages=True)
    async def panda(self,ctx):
        '''
        Get random panda images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/panda")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))

    @commands.command(aliases=['redpandaimage'])
    @commands.bot_has_permissions(send_messages=True)
    async def redpanda(self,ctx):
        '''
        Get random redpanda images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/red_panda")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))

    @commands.command(aliases=['birdimage'])
    @commands.bot_has_permissions(send_messages=True)
    async def bird(self,ctx):
        '''
        Get random bird images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/birb")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))

    @commands.command(aliases=['foximage'])
    @commands.bot_has_permissions(send_messages=True)
    async def fox(self,ctx):
        '''
        Get random fox images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/fox")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))

    @commands.command(aliases=['koalaimage'])
    @commands.bot_has_permissions(send_messages=True)
    async def koala(self,ctx):
        '''
        Get random koala images
        '''
        data = fetch_json(url="https://some-random-api.ml/img/koala")
        await ctx.send(embed=await basic_image1(ctx=ctx,bot=self.bot,image_url=data['link']))

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def wink(self,ctx,user:discord.User):
        '''
        Wink at any user
        '''
        data = fetch_json(url="https://some-random-api.ml/animu/wink")
        await ctx.send(embed=await basic_image2(ctx=ctx,bot=self.bot,image_url=data['link'],text=f"{ctx.message.author.name} winks at {user.name}"))

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def pat(self,ctx,user:discord.User):
        '''
        Pat a user for their job.
        '''
        data = fetch_json(url="https://some-random-api.ml/animu/pat")
        await ctx.send(embed=await basic_image2(ctx=ctx,bot=self.bot,image_url=data['link'],text=f"{ctx.message.author.name} pats {user.name}"))

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def hug(self,ctx,user:discord.User):
        '''
        Hug any user
        '''
        data = fetch_json(url="https://some-random-api.ml/animu/hug")
        await ctx.send(embed=await basic_image2(ctx=ctx,bot=self.bot,image_url=data['link'],text=f"{ctx.message.author.name} hugs {user.name}"))

    # @commands.command(aliases=['colourfull'])
    # @commands.bot_has_permissions(send_messages=True)
    # async def colorfull(self,ctx,user:discord.User=None):
    #     user = user or ctx.message.author
    #     res = requests.get("https://some-random-api.ml/canvas/gay?avatar=https://cdn.discordapp.com/avatars/766553763569336340/cd87cf912f7934d2b1d167cbf9cead12.png?size=1024")
    #     THMB = res.content
    #     stream = io.BytesIO(THMB)
    #     e=discord.Embed(title=" ")
    #     file = discord.File(stream,'abc.png')
    #     e.set_image(url="attachment://abc.png")
    #     await ctx.send(embed=e,file=file)

    @commands.command(aliases=['colourfull'])
    @commands.bot_has_permissions(send_messages=True)
    async def colorfull(self,ctx,user:discord.User=None):
        '''
        Make any image full of colours
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/gay?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def glass(self,ctx,user:discord.User=None):
        '''
        Applies glassy effect to an image
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/glass?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def wasted(self,ctx,user:discord.User=None):
        '''
        That GTA V wasted effect to any users avatar
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command(aliases=['trigger'])
    @commands.bot_has_permissions(send_messages=True)
    async def triggered(self,ctx,user:discord.User=None):
        '''
        Triggered effect to user's avatar
        '''
        user = user or ctx.message.author
        await bytes_gif(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/triggered?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def greyscale(self,ctx,user:discord.User=None):
        '''
        Converts user's avatar in greyscale
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/greyscale?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def invert(self,ctx,user:discord.User=None):
        '''
        Invert the color of any user's avatar
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/invert?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def invertgs(self,ctx,user:discord.User=None):
        '''
        Invert any user's avatar to greyscale 
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/invertgreyscale?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def brightness(self,ctx,user:discord.User=None):
        ''' Increase the brightness of any user's avatar '''
        user = user or ctx.message.authors
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/brightness?avatar={user.avatar_url_as(format='png')}",user=user)
    
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def threshold(self,ctx,user:discord.User=None):
        '''
        Apply threshold to any user's avatar
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/threshold?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def sepia(self,ctx,user:discord.User=None):
        ''' Apply sepia effect to any user's avatar '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/sepia?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def red(self,ctx,user:discord.User=None):
        '''
        Convert user's avatar to red color
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/red?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def green(self,ctx,user:discord.User=None):
        '''
        Convert user's avatar to green color
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/green?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def blue(self,ctx,user:discord.User=None):
        '''
        Convert user's avatar to blue color
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/blue?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command(aliases=['coloured'])
    @commands.bot_has_permissions(send_messages=True)
    async def colored(self,ctx,color,user:discord.User=None):
        '''
        Convert any user's avatar to any color you want to
        '''
        user = user or ctx.message.author
        if "0x" in color:
            color = color.replace("0x","")
        if "#" in color:
            color = color.replace("#","")
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/color?avatar={user.avatar_url_as(format='png')}&color={color}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def pixelate(self,ctx,user:discord.User=None):
        '''
        Pixelate any user's avatar
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/pixelate?avatar={user.avatar_url_as(format='png')}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def ytcomment(self,ctx,user:discord.User=None,*,comment:str):
        '''
        YouTube comment image manupilator
        '''
        user = user or ctx.message.author
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://some-random-api.ml/canvas/youtube-comment?avatar={user.avatar_url_as(format='png')}&comment={comment}&username={user.name}",user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def threat(self,ctx,user:discord.User=None):
        '''
        Declare someone as threat
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=threats&url={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def baguette(self,ctx,user:discord.User=None):
        '''
        Convert user to a baugette
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=baguette&url={user.avatar_url}")
        url = data['message']
        await bytes_image2(ctx=ctx,bot=self.bot,url=url,user=user,text="How's that baguette?")
    
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def clyde(self,ctx,*,msg):
        ''' Sends any message as clyde '''
        user = ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=clyde&text={msg}")
        url = data['message']
        await bytes_image2(ctx=ctx,bot=self.bot,url=url,user=user,text="Cylde wants to say something ...")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def ship(self,ctx,user1:discord.User,user2:discord.User):
        '''
        Ship two users
        '''
        user = ctx.message.author
        user1 = user1 or ctx.message.author
        user2 = user2 or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=ship&user1={user1.avatar_url}&user2={user2.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def captcha(self,ctx,user:discord.User=None):
        '''
        Get the captcha of any user's avatar
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=captcha&url={user.avatar_url}&username={user.name}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def whowouldwin(self,ctx,user1:discord.User,user2:discord.User):
        ''' Who would win image '''
        user = ctx.message.author
        user1 = user1 or ctx.message.author
        user2 = user2 or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={user1.avatar_url}&user2={user2.avatar_url}")
        url = data['message']
        await bytes_image2(ctx=ctx,bot=self.bot,url=url,user=user,text="Lets see..")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def changemymind(self,ctx,*,msg):
        '''
        Changemymind image manupilation
        '''
        user = ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=changemymind&text={msg}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def lolice(self,ctx,user:discord.User=None):
        '''
        Want to get hired in lolice?
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=lolice&url={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def kannafy(self,ctx,*,msg):
        '''  '''
        user = ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=kannagen&text={msg}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def iphone(self,ctx,user:discord.User=None):
        '''
        Get your face in an I-Phone X
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=iphonex&url={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    # @commands.command() #----------> API made it depriciated so no use
    # @commands.bot_has_permissions(send_messages=True)
    # async def kms(self,ctx,user:discord.User=None):
    #     user = user or ctx.message.author
    #     data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=kms&url={user.avatar_url}")
    #     url = data['message']
    #     await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def animeface(self,ctx,user:discord.User=None):
        '''
        Makes you an anime character
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=animeface&url={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def awooify(self,ctx,user:discord.User=None):
        ''' Awooifys user's avatar '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=awooify&url={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def trap(self,ctx,user:discord.User):
        '''
        Trap a user in a trapcard
        '''
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=trap&name={user.name}&author={ctx.message.author.name}&image={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    # @commands.command()
    # @commands.bot_has_permissions(send_messages=True)
    # async def nichijou(self,ctx,*,msg):
    #     user = ctx.message.author
    #     data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=nichijou&text={msg}")
    #     url = data['message']
    #     await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def trumptweet(self,ctx,*,msg):
        '''
        Make trump tweet what you want
        '''
        user = ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={msg}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def tweet(self,ctx,user:discord.User,*,msg):
        '''
        Tweet!
        '''
        # user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=tweet&username={user.name}&text={msg}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    # @commands.command() # TODO - Recheck this once
    # @commands.bot_has_permissions(send_messages=True)
    # async def kidnap(self,ctx,user:discord.User):
    #     # user = user or ctx.message.author
    #     data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=kidnap&image={user.avatar_url_as(format='png')}")
    #     url = data['message']
    #     await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def deepfry(self,ctx,user:discord.User):
        '''
        Deepfry an user's avatar
        '''
        # user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=deepfry&image={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def blurpify(self,ctx,user:discord.User):
        '''
        Blurpify effect
        '''
        # user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=blurpify&image={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def magik(self,ctx,intensity:int,*,user:discord.User=None):
        ''' This command realy does a magic. Make sure to enter intensity as number between 1 to 9 '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=magik&image={user.avatar_url_as(format='png')}&intensity={intensity}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def stickbug(self,ctx,user:discord.User=None):
        '''
        Stick a bug
        '''
        user = user or ctx.message.author
        data = fetch_json(url=f"https://nekobot.xyz/api/imagegen?type=stickbug&url={user.avatar_url}")
        url = data['message']
        await bytes_image(ctx=ctx,bot=self.bot,url=url,user=user)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def gdfont(self,ctx,font:int,*,text:str):
        '''
        Get your font nicely decorated. Font must be a number
        '''
        if font <= 0 or font > 12:
            return await ctx.send(f"{cross} | Please enter font between 1 and 12.")
        await bytes_image(ctx=ctx,bot=self.bot,url=f"https://gdcolon.com/tools/gdfont/img/{text}?font={font}",user=None)

    

def setup(bot):
    bot.add_cog(Images(bot))
    print(Fore.GREEN + "[STATUS OK] Image cog is ready!")