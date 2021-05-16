import discord
from discord.ext import commands
import asyncio
from cogs.utils import ethrow,emoji
import os
import inspect
from cogs.utils.paginator1 import WrappedPaginator,PaginatorInterface
from cogs.utils.models import copy_context_with
from cogs.utils.exception_handling import ReplResponseReactor
import time
import collections
import mystbin
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

class Debug(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    __all__ = (
    'Feature',
    'CommandTask'
    )

    CommandTask = collections.namedtuple("CommandTask", "index ctx task")

    def submit(self, ctx: commands.Context):
        """
        A context-manager that submits the current task to jishaku's task list
        and removes it afterwards.
        Parameters
        -----------
        ctx: commands.Context
            A Context object used to derive information about this command task.
        """

        self.task_count += 1

        try:
            current_task = asyncio.current_task()  # pylint: disable=no-member
        except RuntimeError:
            # asyncio.current_task doesn't document that it can raise RuntimeError, but it does.
            # It propagates from asyncio.get_running_loop(), so it happens when there is no loop running.
            # It's unclear if this is a regression or an intentional change, since in 3.6,
            #  asyncio.Task.current_task() would have just returned None in this case.
            current_task = None

        cmdtask = CommandTask(self.task_count, ctx, current_task)

        self.tasks.append(cmdtask)

        try:
            yield cmdtask
        finally:
            if cmdtask in self.tasks:
                self.tasks.remove(cmdtask)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def distruct(self,ctx):
        # await ctx.channel.purge(limit=1)
        destruct_time = 5
        message = await ctx.send(f"Self-destructing in - {destruct_time} seconds")
        while True:
            destruct_time -= 1
            if destruct_time == 0:
                await ctx.send(f"Bot is now down! 👋🏻")
                break
            await message.edit(content=f"Self-destructing in - {destruct_time} seconds")
            await asyncio.sleep(1)
        quit()
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self,ctx,name:str):
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(ethrow.traceback_throw(e))
        await ctx.send(f"{emoji.tick} | Loaded extension **{name}**")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self,ctx,name:str):
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(ethrow.traceback_throw(e))
        await ctx.send(f"{emoji.tick} | Unloaded extension **{name}**")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self,ctx,name:str):
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(ethrow.traceback_throw(e))
        await ctx.send(f"{emoji.tick} | Reloaded extension **{name}**")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def trace(self,ctx,flag:int = 0):
        try:
            if self.bot.tr is None:
                await ctx.send("There are no tracebacks happened!")
        except:
            await ctx.send("There are no current exceptions happened!")
        if flag == 0:
            me = self.bot.get_user(766553763569336340)
            return await me.send(f"```py\n{self.bot.tr}\n```")
        else:
            return await ctx.send(f"```py\n{self.bot.tr}\n```")

    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def source(self,ctx,*,command_name:str):
    #     command = self.bot.get_command(command_name)
    #     if not command:
    #         return await ctx.send(f"{emoji.cross} | Couldn't find command `{command_name}`")
    #     try:
    #         source_lines, _ = inspect.getsourcelines(command.callback)
    #     except(TypeError, OSError):
    #         return await ctx.send(f"{emoji.cross} | Unable to retrieve the source for `{command}` for some reason.")
    #     source_lines = ''.join(source_lines).split('\n')
    #     paginator = WrappedPaginator(prefix='```py',suffix='```',max_size=1985)
    #     for line in source_lines:
    #         paginator.add_line(discord.utils.escape_markdown(line))
    #     interface = PaginatorInterface(ctx.bot,paginator,owner=ctx.author)
    #     await interface.send_to(ctx)

    @commands.command()
    @commands.is_owner()
    async def debug(self,ctx,*,command_string:str):
        alt_ctx = await copy_context_with(ctx,content=ctx.prefix+command_string)
        if alt_ctx.command is None:
            return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')
        start = time.perf_counter()
        async with ReplResponseReactor(ctx.message):
            with self.submit(ctx):
                await alt_ctx.command.invoke(alt_ctx)
        end = time.perf_counter()
        return await ctx.send(f"Command `{alt_ctx.command.qualified_name}` finished in {end-start:.3f}s")

    
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def logs(self,ctx):
        with open('thecoderzbot.log','r') as f:
            content = f.read()
        mystbin_client = mystbin.Client()
        paste = await mystbin_client.post(content,syntax="log")
        url = paste.url
        em = discord.Embed(title="Here are the logs. I have pasted it in the bin due to its size",description=f"[Click here to see]({url})",color=await fetch_color(bot=self.bot,ctx=ctx))
        em.set_footer(text=f"Requested by - {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
        em.add_field(name=f"{emoji.rps} Note: ",value="Whenever someone uses this command this is reported to the owner. So be carefull your information has been reached to the owner of this bot",inline=False)
        await ctx.send(embed=em)
        me = discord.utils.get(self.bot.users,id=self.bot.owner_id)
        await me.send(f"{ctx.message.author.name}#{ctx.message.author.discriminator} `[{ctx.message.author.id}]` used log command to view logs.")


    #========= Not done======#
    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self,ctx):
        pass
    
    #======================#

def setup(bot):
    bot.add_cog(Debug(bot))
    print(OKGREEN + "[STATUS OK] Debug cog is ready!")