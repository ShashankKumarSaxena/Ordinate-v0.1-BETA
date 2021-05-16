import discord
from discord.ext import commands
import requests
import random
import json
from cogs.utils.emoji import cross,qcross,qtick
from colorama import init,Fore
from cogs.utils.color import fetch_color
from cogs.utils.api_fetcher import fetch_json
import alexflipnote
from cogs.utils.confimation import confirmation
from translate import Translator

init(autoreset=True)

class API(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    alex_api = alexflipnote.Client("ALEX FLIP NOTE API TOKEN!")
    
    #====== Tenor gif fetcher ======#

    @commands.command()
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def gif(self,ctx,*,search_term):
        ''' Get a random gif of any search term. '''
        if search_term is None or search_term == "":
            return await ctx.send(f"{cross} | Please enter a valid search term")
        apikey = "30URSCO95UX4"
        lmt = 10
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        if r.status_code == 200:
            top_10gifs = json.loads(r.content)
            if not top_10gifs:
                return await ctx.send(f"{cross} | No gif found for {ctx.message.text}")
            rval = random.randint(0,10)
            url_fetch = top_10gifs["results"][rval]["media"][0]["gif"]["url"]
            em = discord.Embed(description=" ",color=await fetch_color(bot=self.bot,ctx=ctx))
            em.set_image(url=url_fetch)
            em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
            # return await ctx.send(url_fetch)
            return await ctx.send(embed=em)
        else:
            return await ctx.send(f"{cross} | Sorry nothing found for `{search_term}`")

    #===============================#

    #========== Figlet =============#

    @commands.command()
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def figlet(self,ctx,*,text):
        ''' Get your text decorated in ascii '''
        res = requests.get(f"https://artii.herokuapp.com/make?text={text}")
        await ctx.send(f"```\n{res.text}\n```")

    #===============================#

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def rgbtohex(self,ctx,*,rgbval):
        ''' Convert RGB values to hex'''
        if "(" in rgbval and ")" in rgbval:
            rgbval = rgbval.replace("(","")
            rgbval = rgbval.replace(")","")
        r,g,b = rgbval.split(',')
        res = json.loads(requests.get(f"https://some-random-api.ml/canvas/hex/?rgb={r},{g},{b}").text)
        try:
            if res['error']:
                return await ctx.send(f"{cross} | Please enter a valid value")
        except:
            pass
        await ctx.send(f"Hex value - {res['hex']}")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def hextorgb(self,ctx,*,hexval):
        ''' Convert hex value to RGB '''
        if "0x" in hexval:
            hexval = hexval.replace("0x","")
        if "#" in hexval:
            hexval = hexval.replace("#","")
        res = json.loads(requests.get(f"https://some-random-api.ml/canvas/rgb/?hex={hexval}").text)
        if res['error']:
            return await ctx.send(f"{cross} | Please enter a valid value")
        await ctx.send(f"RGB value - `{res['r']},{res['g']},{res['b']}`")

    @commands.command(aliases=['viewcolour'])
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def viewcolor(self,ctx,hexval):
        ''' View any color by passing hex value '''
        if "0x" in hexval:
            hexval = hexval.replace("0x","")
        if "#" in hexval:
            hexval = hexval.replace("#","")
        res = requests.get(f"https://some-random-api.ml/canvas/colorviewer/?hex={hexval}").url
        if res is None:
            return await ctx.send(f"{cross} | Please enter a valid value")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(description=f"Color : #{hexval}",color=color)
        em.set_image(url=res)
        await ctx.send(embed=em)
        
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def encodebinary(self,ctx,*,text):
        ''' Encode text to binary '''
        res = json.loads(requests.get(f"https://some-random-api.ml/binary?text={text}").text)
        await ctx.send(f"Binary of {text} : `{res['binary']}`")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def decodebinary(self,ctx,*,binary):
        ''' Decode binary to text '''
        if 0 in binary or 1 in binary:
            res = json.loads(requests.get(f"https://some-random-api.ml/binary?decode={binary}").text)
            await ctx.send(f"Decode of entered binary - `{res['text']}`")
        else:
            return await ctx.send(f"{cross} | Please enter a valid binary")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def encode(self,ctx,*,text):
        ''' Encode text to base64 encryption '''
        res = json.loads(requests.get(f"https://some-random-api.ml/base64?encode={text}").text)
        try:
            if res['error']:
                return await ctx.send(f"{cross} | Please enter a valid value")
        except KeyError:
            pass
        await ctx.send(f"Encoded value of {text} - `{res['base64']}`")
    
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def decode(self,ctx,*,text):
        ''' Decode base64 encryption to text '''
        res = json.loads(requests.get(f"https://some-random-api.ml/base64?decode={text}").text)
        try:
            if res['error']:
                return await ctx.send(f"{cross} | Please enter a valid value")
        except KeyError:
            pass
        await ctx.send(f"Decoded value of {text} - `{res['text']}`")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def dogfact(self,ctx):
        ''' Get random dog facts '''
        result = fetch_json(url="https://some-random-api.ml/facts/dog")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title="Dog facts",description=f"{result['fact']}",color=color)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)
    
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def catfact(self,ctx):
        ''' Get random cat facts '''
        result = fetch_json(url="https://some-random-api.ml/facts/cat")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title="Cat facts",description=f"{result['fact']}",color=color)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def pandafact(self,ctx):
        ''' Get random panda facts '''
        result = fetch_json(url="https://some-random-api.ml/facts/panda")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title="Panda facts",description=f"{result['fact']}",color=color)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def foxfact(self,ctx):
        ''' Get random fox facts '''
        result = fetch_json(url="https://some-random-api.ml/facts/fox")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title="Fox facts",description=f"{result['fact']}",color=color)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def birdfact(self,ctx):
        ''' Get random birds fact '''
        result = fetch_json(url="https://some-random-api.ml/facts/bird")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title="Bird facts",description=f"{result['fact']}",color=color)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def koalafact(self,ctx):
        ''' Get random koala facts '''
        result = fetch_json(url="https://some-random-api.ml/facts/koala")
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title="Koala facts",description=f"{result['fact']}",color=color)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(aliases=['colourinfo'])
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(send_messages=True)
    async def colorinfo(self,ctx,color):
        ''' Get information about a color. Pass the value in hex format. '''
        if "0x" in color:
            color = color.replace("0x","")
        if "#" in color:
            color = color.replace("#","")
        fetched_color = await self.alex_api.colour(color)
        embed_color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(description=" ",color=embed_color)
        em.add_field(name="Name",value=fetched_color.name,inline=True)
        em.add_field(name="HEX",value=fetched_color.hex,inline=True)
        em.add_field(name="RGB",value=fetched_color.rgb,inline=True)
        em.add_field(name="Int",value=fetched_color.int,inline=True)
        em.add_field(name="Brightness",value=fetched_color.brightness,inline=True)
        em.set_thumbnail(url=fetched_color.image)
        em.set_image(url=fetched_color.image_gradient)
        await ctx.send(embed=em)
        

    # Weather api
    # use some modules bruh
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_guild_permissions(send_messages=True)
    async def weather(self,ctx,*,location):
        ''' Get weather info of any location '''
        data = fetch_json(url=f"http://api.weatherstack.com/current?access_key=af5143c8ee74d880104cc744a5b0f5a4&query={location}")
        try:
            color = await fetch_color(bot=self.bot,ctx=ctx)
            em = discord.Embed(title=f"Weather of {data['request']['query']}",color=color)
            em.add_field(name="Temperature",value=data['current']['temperature'])
            em.add_field(name="Weather code",value=data['current']['weather_code'])
            em.add_field(name="Time",value=data['location']['localtime'])
            em.add_field(name="Wind speed",value=data['current']['wind_speed'])
            em.add_field(name="Wind degree",value=data['current']['wind_degree'])
            em.add_field(name="Wind direction",value=data['current']['wind_dir'])
            em.add_field(name="Pressure",value=data['current']['pressure'])
            em.add_field(name="Humidity",value=data['current']['humidity'])
            em.add_field(name="Cloud cover",value=data['current']['cloudcover'])
            em.add_field(name="Feels like",value=data['current']['feelslike'])
            em.add_field(name="UV index",value=data['current']['uv_index'])
            em.add_field(name="Day?",value=data['current']['is_day'])
            em.set_thumbnail(url=data['current']['weather_icons'][0])
            em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=em)
        except:
            return await ctx.send(f"{cross} | Nothing found for entered query.")

    #=========== TODO - Gonna fix it soon ==========#
    @commands.command(aliases=['tr','translator'])
    @commands.has_permissions(send_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def translate(self,ctx,lang,*,msg):
        ''' Translate english to any other language '''
        translator = Translator(to_lang=lang)
        translation = translator.translate(msg)
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(description=" ",color=color)
        em.add_field(name="Original",value=f"```\n{msg}\n```",inline=False)
        em.add_field(name="Translation",value=f"```\n{translation}\n```",inline=False)
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def meme(self,ctx):
        ''' Get a exotic meme '''
        # data = fetch_json(url="https://memes.blademaker.tv/api")
        while True:
            r = requests.get("https://memes.blademaker.tv/api")
            data = r.json()
            if data['nsfw'] == False:
                break
        # r = requests.get("https://memes.blademaker.tv/api?lang=en")
        # data = r.json()
        color = await fetch_color(bot=self.bot,ctx=ctx)
        em = discord.Embed(title=f"{data['title']}",color=color)
        em.set_image(url=data['image'])
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)
    


def setup(bot):
    bot.add_cog(API(bot))
    print(Fore.GREEN + "[STATUS OK] API cog is ready!")