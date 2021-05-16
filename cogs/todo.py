import discord
from discord.ext import commands
import asyncpg
from cogs.utils.emoji import cross, tick
from colorama import Fore, init
from cogs.utils.lister import lister_str
from cogs.utils.color import fetch_color

init(autoreset=True)


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.bot.loop.create_task(self.setup())

    @commands.group(pass_context=True)
    @commands.bot_has_permissions(send_messages=True)
    async def todo(self, ctx):
        ''' Your todo manager '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    @todo.command(pass_context=True,
                  aliases=['todo_add'])
    @commands.bot_has_permissions(send_messages=True)
    async def add(self, ctx, *, task):
        ''' Add any task in the todo list '''
        if len(task) > 100:
            return await ctx.send(f"{cross} | You cannot enter a task with more than 100 length")
        todo_red_list = await self.bot.testdb1.fetch("SELECT content FROM todo WHERE user_id = $1", ctx.author.id)
        todo_list = [r['content'] for r in todo_red_list]
        if task in todo_list:
            return await ctx.send(f"{cross} | You already have that task in the list!")
        await self.bot.testdb1.execute("INSERT INTO todo (user_id,content) VALUES ($1,$2)", ctx.author.id, str(task))
        await ctx.send(f"{tick} | Todo added successfully!")

    @todo.command(pass_context=True,
                  aliases=['todo_list'])
    @commands.bot_has_permissions(send_messages=True)
    async def list(self, ctx):
        ''' List your todos '''
        todo_red_list = await self.bot.testdb1.fetch("SELECT content FROM todo WHERE user_id = $1", ctx.author.id)
        todo_list = [r['content'] for r in todo_red_list]
        if not todo_red_list:
            return await ctx.send(f"{cross} | You don't have any todos added!")
        # await ctx.send(todo_list)
        await lister_str(
            ctx=ctx,
            your_list=todo_list,
            color=await fetch_color(bot=self.bot, ctx=ctx),
            title=f"Todo list of {ctx.author.name}"
        )

    @todo.command(pass_context=True,
                  aliases=['todo_remove'])
    @commands.bot_has_permissions(send_messages=True)
    async def remove(self, ctx, *, todo):
        ''' Remove any task from the todo list '''
        await self.bot.testdb1.execute("DELETE FROM todo WHERE user_id = $1 AND content = $2", ctx.author.id, todo)
        await ctx.send(f"{tick} | Todo has been removed successfully!")

    @todo.command(pass_context=True,
                  aliases=['todo_clear'])
    @commands.bot_has_permissions(send_messages=True)
    async def clear(self, ctx):
        ''' Clears the todo list '''
        await self.bot.testdb1.execute("DELETE FROM todo WHERE user_id = $1", ctx.author.id)
        await ctx.send(f"{tick} | Your todos has been cleared!")

    async def setup(self) -> None:
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS todo (user_id bigint, content character varying)")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()


def setup(bot):
    bot.add_cog(Todo(bot))
    print(Fore.GREEN + "[STATUS OK] Todo cog is ready!")
