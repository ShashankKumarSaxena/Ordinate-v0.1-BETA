import discord
from discord.ext import commands
from cogs.utils.lister import lister
from cogs.utils.color import fetch_color

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Category(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(pass_context=True)
    # @commands.has_permissions(manage_channels=True)
    # @commands.bot_has_permissions(manage_channels=True)
    async def category(self,ctx):
        ''' Category management commands '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    @category.command(pass_context=True)
    @commands.has_permissions(
        send_messages=True
    )
    async def list(self,ctx):
        ''' This command will list all the categories in the guild '''
        if len(ctx.guild.categories) == 0:
            await ctx.send("There are no categories in this guild.")
        # e = discord.Embed(
        #     title=f"Categories in {ctx.guild.name}",
        #     description='n'.join(f"• {category}" for category in ctx.guild.categories),
        #     color=discord.Color.purple()
        # )
        # e.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        # e.set_footer(text="Type `s!help <command_name>` to get detailed help")
        # await ctx.send(embed=e)
        await lister(ctx=ctx,your_list=ctx.guild.categories,color=await fetch_color(bot=self.bot,ctx=ctx),title=f"List of categories in {ctx.guild.name}")


    @category.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def create(self,ctx,*,name):
        ''' Create a category with this command '''
        if name is not None:
            await ctx.guild.create_category(name,overwrites=None,reason=None)
            await ctx.send(f"Category **{name}** has been created!")

    @category.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def delete(self,ctx,*,name):
        ''' Delete a category. Make sure to enter the name only! '''
        # print(ctx.guild.categories)
        channel = discord.utils.get(ctx.guild.categories,name=name)
        if channel is not None:
            await channel.delete(reason=None)
            await ctx.send(f"Category **{name}** deleted")
        if channel is None:
            await ctx.send("Please enter valid category name!")

    

    @category.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def rename(self,ctx,category_name,*,new_name):
        ''' Rename a category. Make sure to enter the name only! '''
        category = discord.utils.get(ctx.guild.categories,name=category_name)
        if category is not None:
            await category.edit(name=new_name)  
            await ctx.send(f"Category **{category_name}** renamed to **{new_name}**")
        if category is None:
            await ctx.send(f"No category named **{category_name}** found in guild!")


    @category.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def channels(self,ctx,*,category_name:str=None):
        ''' This command will give list of channels in a category '''
        if category_name is not None and category_name not in ctx.guild.categories:
            await ctx.send("Please enter a valid category name.")
        category = category or ctx.channel.category
        # elif category_name is not None:
        #     category = discord.utils.get(ctx.guild.categories,name=category_name)
        #     e = discord.Embed(
        #         title=f"Channel list in category : {category}",
        #         color=discord.Color.purple()
        #     )
        #     e.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        #     if len(category.channels) == 0:
        #         await ctx.send(f"No channels found in category **{category}**")
        #     else:
        #         e.description = '\n'.join(f"• {channel}" for channel in category.channels)
        #         e.set_footer(text="Type `s!help <command_name>` to get detailed help")
        #         await ctx.send(embed=e)
    
        # elif category_name is None:
        #     category = ctx.channel.category
        #     e = discord.Embed(
        #         title=f"Channel list in category {category}",
        #         description='\n'.join(f"• {channel}" for channel in category.channels),
        #         color=discord.Color.purple()
        #     )
        #     e.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        #     if len(category.channels) == 0:
        #         await ctx.send(f"No channels found in category **{category}**")
        
        #     e.set_footer(text="Type `s!help <command_name>` to get detailed help")
        #     await ctx.send(embed=e)
        await lister(ctx=ctx,your_list=category.channels,color=await fetch_color(bot=self.bot,ctx=ctx))
    

    @category.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def hide(self,ctx,*,category_name:str=None):
        ''' Hide a category from the server '''
        if category_name is not None:
            category = discord.utils.get(ctx.guild.categories,name=category_name)
            if category is None:
                return await ctx.send(f"No category named {category_name} found in guild!")
            else:
                for text_channel in category.text_channels:
                    await text_channel.set_permissions(ctx.guild.default_role,view_channel=False)
                for voice_channel in category.voice_channels:
                    await voice_channel.set_permissions(ctx.guild.default_role,connect=False)
            await ctx.send(f"**Category : {category_name}** successfully hidden!")
        elif category_name is None:
            category = ctx.channel.category
            for text_channel in category.text_channels:
                await text_channel.set_permissions(ctx.guild.default_role,view_channel=False)
            for voice_channel in category.voice_channels:
                await voice_channel.set_permissions(ctx.guild.default_role,connect=False)
            await ctx.send(f"**Category : {category_name}** successfully hidden!")



    @category.command(pass_context=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def unhide(self,ctx,*,category_name:str=None):
        ''' Unhide the category from the server '''
        if category_name is not None:
            category = discord.utils.get(ctx.guild.categories,name=category_name)
            if category is None:
                return await ctx.send(f"No category named {category_name} found in guild!")
            else:
                for text_channel in category.text_channels:
                    await text_channel.set_permissions(ctx.guild.default_role,view_channel=True)
                for voice_channel in category.voice_channels:
                    await voice_channel.set_permissions(ctx.guild.default_role,connect=True)
            await ctx.send(f"Category : **{category_name}** successfully unhidden!")
        elif category_name is None:
            category = ctx.channel.category
            for text_channel in category.text_channels:
                await text_channel.set_permissions(ctx.guild.default_role,view_channel=True)
            for voice_channel in category.voice_channels:
                await voice_channel.set_permissions(ctx.guild.default_role,connect=True)
            await ctx.send(f"Category : **{category_name}** successfully unhidden!")


def setup(bot):
    bot.add_cog(Category(bot))
    print(OKGREEN + "[STATUS OK] Category is ready")
