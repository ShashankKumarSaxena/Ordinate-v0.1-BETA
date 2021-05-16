import discord
from discord.ext import commands
from colorama import init,Fore
from cogs.utils.color import fetch_color
import asyncio

init(autoreset=True)

class Ticket(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def ticket(self,ctx):
        ''' Creates tickets '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
            await ctx.send_help(helper)

    @ticket.command(pass_context=True)
    async def new(self, ctx, *, args=None):
        ''' Creates a new ticket '''
        await self.bot.wait_until_ready()
        if args is None:
            message_content = "Please wait, we will be with you shortly"
        else:
            message_content = "".join(args)

        ticket_channel = await ctx.guild.create_text_channel(
            f"{ctx.author.name}-ticket"
        )

        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id),
                                             send_messages=False,
                                             read_messages=False)

        await ticket_channel.set_permissions(ctx.author,
                                             send_messages=True,
                                             read_messages=True,
                                             embed_links=True,
                                             add_reactions=True,
                                             attach_files=True,
                                             read_message_history=True)

        em = discord.Embed(title=f"Ticket from {ctx.author.name}#{ctx.author.discriminator}",
                            description=f"{message_content}",
                            color=await fetch_color(bot=self.bot,ctx=ctx)
                            )

        await self.bot.testdb1.execute("INSERT INTO ticketdata(guild_id,channel_id) VALUES ($1,$2)",
                                       ctx.guild.id, ticket_channel.id)

        await ticket_channel.send(embed=em)

        created_em = discord.Embed(title="Tickets",
                                    description=f"Your ticket has been created at {ticket_channel.mention}",
                                    color=await fetch_color(bot=self.bot,ctx=ctx)
                                    )
        await ctx.send(embed=created_em)

    @ticket.command()
    @commands.has_permissions(administrator=True)
    async def close(self, ctx):
        ''' Closes the open ticket '''
        channel_ids_rec = await self.bot.testdb1.fetch("SELECT channel_id FROM ticketdata WHERE guild_id = $1",ctx.guild.id)
        channel_ids = []
        for chid in channel_ids_rec:
            channel_ids.append(chid['channel_id'])
        if ctx.channel.id in channel_ids:
            channel_id = ctx.channel.id

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

            try:
                em = discord.Embed(title="Tickets",description='Are you sure you want to close this ticket? Reply with `close` if you are sure.',
                                   color=await fetch_color(bot=self.bot, ctx=ctx))

                await ctx.send(embed=em)
                await self.bot.wait_for('message', check=check, timeout=60)

                await ctx.channel.delete()
                await self.bot.testdb1.execute("DELETE FROM ticketdata WHERE guild_id = $1 AND channel_id = $2",
                                               ctx.guild.id, ctx.channel.id)

            except asyncio.TimeoutError:
                em = discord.Embed(title="Tickets",description="You have run out of time to close this ticket! Please run the command again.",
                                   color=await fetch_color(bot=self.bot, ctx=ctx))


    async def setup(self):
        await self.bot.testdb1.execute("CREATE TABLE IF NOT EXISTS ticketdata(guild_id bigint,channel_id bigint)")


    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup()
    

def setup(bot):
    bot.add_cog(Ticket(bot))
    print(Fore.GREEN+"[STATUS OK] Ticket cog is ready!")
