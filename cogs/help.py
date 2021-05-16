import discord
from discord.ext import commands
from cogs.utils import emoji
from cogs import moderation,images,fun,giveaway,role,setup,todo,ticket,nqn,others,automeme,levelling,isupport,afk,embeds,api,lockdown,category,create,reactionroles,statistics,logs
from cogs import setup as seter
import config
from colorama import init, Fore
from disputils import BotEmbedPaginator

init(autoreset=True)

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attr={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category'
        })

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))
    
    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    def common_command_formatting(self, embed_like, command):
        embed_like.title = self.get_command_signature(command)
        if command.description:
            embed_like.description = f"{command.description}\n\n{command.help}"
        else:
            embed_like.description = command.help or 'No help found.'
        embed_like.add_field(name="Aliases",value=f" | ".join(
            [f"`{alias}`" for alias in command.aliases]) if command.aliases else f"`{command.name}`")
        embed_like.add_field(
            name="Usage", value=f"`{self.get_command_signature(command)}`",inline=False)

    async def send_command_help(self,command):
        embed = discord.Embed(color=discord.Color.orange())
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)
    
    async def send_bot_help(self, mapping):
        bot = self.context.bot
        embed0 = discord.Embed(description="```diff\n- [] = Optional Argument\n- <> = Required Argument\n+ Type o!help [command | module] for more help on a command or module\nDo not type these while using commands!\n```",color=discord.Color.orange())
        embed0.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed0.add_field(name="Modules"
                        ,value=
                                f"{emoji.ani_mod} Moderation • `Page 1`\n"
                                +f"{emoji.ani_uti} Utilities • `Page 2`\n"
                                +f"👉 Others • `Page 3`\n"
                                +f"📸 Images • `Page 4`\n"
                                +f"🎲 Fun • `Page 5`\n"
                                +f"🎉 Giveaway • `Page 6`\n"
                                )
        embed0.add_field(name=f"Official Links",
                        value=f"🤖 [`Official Invite Link`]({config.INVITE_LINK})\n"
                                +f"🔗 [`Official Server Link`]({config.SUPPORT_SERVER_LINK})\n\n"
                                +"**Developer**\n"
                                +f"👑 𝓢𝓬𝔂𝓹𝓱𝓮𝓻#9211")
        # embed0.add_field(name=f"Developer",value=f"👑 𝓢𝓬𝔂𝓹𝓱𝓮𝓻#9211",inline=False)
        embed0.add_field(name=f"Getting Started 👍", value="Use `o!setup command` to fully setup the bot in your server. If any thing you want to ask then you can always use the `o!isupport <issue>` command for an interactive support! Also make sure that the bot has adequeate permissions and role.",inline=False)
        embed0.add_field(name=f"Latest Bot News {emoji.rps}",
                        value=f"{config.BOT_NEWS}",inline=False)

        embed1 = discord.Embed(description=" ",color=discord.Color.orange())
        embed1.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed1.add_field(name="Moderation",
                        value=f",".join(f"`{cmd.name}`" for cmd in moderation.Moderation.get_commands(moderation.Moderation)),inline=False)
        embed1.add_field(name="Channel Manager",value=f",".join(f"`{cmd.qualified_name}`" for cmd in create.Create.walk_commands(create.Create)),inline=False)
        embed1.add_field(name="Category Manager",value=f",".join(f"`{cmd.qualified_name}`" for cmd in category.Category.walk_commands(category.Category)),inline=False)
        embed1.add_field(name="Role",value=f",".join(f"`{cmd.qualified_name}`" for cmd in role.Role.walk_commands(role.Role)))
        embed1.add_field(name="Lockdown",value=f",".join(f"`{cmd.qualified_name}`" for cmd in lockdown.Lockdown.walk_commands(lockdown.Lockdown)),inline=False)

        embed2 = discord.Embed(description=" ",color=discord.Color.orange())
        embed2.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed2.add_field(name="Images",value=f",".join(f"`{cmd.name}`" for cmd in images.Images.get_commands(images.Images)),inline=False)

        embed3 = discord.Embed(description=" ",color=discord.Color.orange())
        embed3.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed3.add_field(name="Fun",value=f",".join(f"`{cmd.name}`" for cmd in fun.Fun.get_commands(fun.Fun)))
        embed3.add_field(name="API",value=f",".join(f"`{cmd.name}`" for cmd in api.API.get_commands(api.API)),inline=False)

        embed4 = discord.Embed(description=" ",color=discord.Color.orange())
        embed4.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed4.add_field(name="Giveaway",value=f",".join(f"`{cmd.name}`" for cmd in giveaway.Giveaway.get_commands(giveaway.Giveaway)))
        
        embed5 = discord.Embed(description=" ",color=discord.Color.orange())
        embed5.add_field(name="Setup",value=f",".join(f"`{cmd.qualified_name}`" for cmd in seter.Setup.walk_commands(seter.Setup)),inline=False)
        embed5.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed5.add_field(name="Interactive Support",value=f",".join(f"`{cmd.name}`" for cmd in isupport.InteractiveSupport.get_commands(isupport.InteractiveSupport)))
        embed5.add_field(name="To-do Manager",value=f",".join(f"`{cmd.qualified_name}`" for cmd in todo.Todo.walk_commands(todo.Todo)),inline=False)
        embed5.add_field(name="Levelling",value=f",".join(f"`{cmd.qualified_name}`" for cmd in levelling.Levelling.walk_commands(levelling.Levelling)),inline=False)
        embed5.add_field(name="Reaction Roles",value=f",".join(f"`{cmd.qualified_name}`" for cmd in reactionroles.ReactionRoles.walk_commands(reactionroles.ReactionRoles)),inline=False) 
        embed5.add_field(name="Stats",value=f",".join(f"`{cmd.qualified_name}`" for cmd in statistics.Stats.walk_commands(statistics.Stats)),inline=False)
        embed5.add_field(name="Logging",value=f",".join(f"`{cmd.qualified_name}`" for cmd in logs.Logs.walk_commands(logs.Logs)),inline=False)


        embed6 = discord.Embed(description=" ",color=discord.Color.orange())
        embed6.set_author(name="Ordinate Commands",icon_url="https://cdn.discordapp.com/avatars/810137345789263913/27d8247b6ba63916d19a4b5974c314e3.png?size=1024")
        embed6.add_field(name="Automeme",value=f",".join(f"`{cmd.qualified_name}`" for cmd in automeme.AutoMeme.walk_commands(automeme.AutoMeme)),inline=False)
        embed6.add_field(name="NQN",value=f",".join(f"`{cmd.qualified_name}`" for cmd in nqn.NQN.walk_commands(nqn.NQN)),inline=False) 
        embed6.add_field(name="AFK",value=f",".join(f"`{cmd.qualified_name}`" for cmd in afk.Afk.walk_commands(afk.Afk)),inline=False)
        embed6.add_field(name="Ticket",value=f",".join(f"`{cmd.qualified_name}`" for cmd in ticket.Ticket.walk_commands(ticket.Ticket)),inline=False)
        embed6.add_field(name="Others",value=f",".join(f"`{cmd.name}`" for cmd in others.Others.get_commands(others.Others)),inline=False)

        # embed7 = discord.Embed(description=" ",color=discord.Color.orange())
        # embed7.set_author(name="The Coderz Bot",icon_url="https://cdn.discordapp.com/avatars/798557068998738000/d42b7eac0a9d8d804112a04b82a95964.png?size=1024")

        # embed8 = discord.Embed(description=" ",color=discord.Color.orange())

        # await self.context.send(embed=embed)
        embeds = [embed0,embed1,embed5,embed6,embed2,embed3,embed4]
        paginator = BotEmbedPaginator(self.context, embeds)
        await paginator.run()

    async def send_group_help(self, cmd):
        e = discord.Embed(color=discord.Color.orange())
        e.title = f"Category: **{cmd.name}**" + \
            (" | " + "-".join(cmd.aliases) if cmd.aliases else "")
        e.set_author(name=self.context.guild.me.display_name,
                    url=f"{config.SUPPORT_SERVER_LINK}",icon_url=self.context.guild.me.avatar_url)
        e.set_footer(text=f"Type o!help <command name> to get more information.")
        cmds = await self.filter_commands(cmd.commands, sort=True)
        for cmd in cmds:
            e.add_field(name=cmd.name + (" | " + '-'.join(cmd.aliases) if cmd.aliases else ""), value=(
                cmd.short_doc if cmd.short_doc else "No description.") + f"\nUsage: `{self.get_command_signature(cmd)}`",inline=False)
        await self.context.send(embed=e)
    
    async def send_cog_help(self, cog):
        embed = discord.Embed(title='{0.qualified_name} Commands'.format(
            cog), color=discord.Color.orange())
        if cog.description:
            embed.description = cog.description
        
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=command.name, value=f"{command.short_doc or '...'}\n"
                                                        f"Usage: `{self.get_command_signature(command)}`", inline=False)
        
        await self.get_destination().send(embed=embed)

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command_cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command



def setup(bot):
    bot.add_cog(Meta(bot))
    print(Fore.GREEN + "[STATUS OK] Meta cog is ready!")
