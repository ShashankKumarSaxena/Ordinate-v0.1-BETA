import discord
from discord.ext import commands,tasks
from cogs.utils.emoji import tick,cross,online,dnd,idle,offline
import math
from disputils import BotEmbedPaginator
import asyncio
import re

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600,"s":1,"m":60,"d":86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key,value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)

class Role(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self,ctx):
        ''' Roles manager category '''
        if ctx.invoked_subcommand is None:
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send(f"{ctx.author.name} The correct way of using this command is ")
            await ctx.send_help(helper)

    @role.command(pass_context=True)
    # @commands.bot_has_permissions(manage_members=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def give(self,ctx,user:discord.Member,role:discord.Role):
        ''' Give a role to any member '''
        if role is None:
            return await ctx.send(f"{cross} | No role named {role} found in this server.")
        await user.add_roles(role)
        await ctx.send(f"{tick} | Role {role.mention} given to {user.mention}")

    @role.command()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def temp(self,ctx,role:discord.Role,time,*,user:discord.Member):
        ''' Temporarily give a role to any member '''
        seconds = convert(time)
        await user.add_roles(role,reason=None)
        await ctx.send(f"{tick} | {role.mention} added to user {user.mention}")
        await asyncio.sleep(seconds)
        await user.remove_roles(role)


    @role.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove(self,ctx,user:discord.Member,role:discord.Role):
        ''' Remove a role from any member '''
        if role is None:
            return await ctx.send(f"{cross} | No role named {role} found in this server.")
        await user.remove_roles(role)
        await ctx.send(f"{tick} | Role {role.mention} removed from {user.mention}")
    

    @role.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def delete(self,ctx,role:discord.Role):
        ''' Deletes the role from server '''
        if role is None:
            return await ctx.send(f"{cross} | No role named {role} found in this server.")
        await role.delete()
        await ctx.send(f"{tick} | Role {role} deleted")


    @role.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def create(self,ctx,*,name):
        ''' Creates a role in the server '''
        await ctx.guild.create_role(name=name,color=discord.Color.default())
        await ctx.send(f"{tick} | Role {name} created successfully!")
        
        # TODO - Make this command so that it can add color to the role

        # if color is None:
        #     await ctx.guild.create_role(name=name,color=discord.Color.default())
        #     await ctx.send(f"Role {name} created successfully!")
        # else:
        #     await ctx.guild.create_role(name=name,color=color)
        #     await ctx.send(f"Role {name} created successfully!")


    @role.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def rename(self,ctx,role:discord.Role,*,newname):
        ''' Renames any role '''
        # BUG - The role with multiple names can't be changed with this
        # prev_name = role.name
        if role is None:
            return await ctx.send(f"{cross} | No role named {role} found in this server.")
        await role.edit(name=newname)
        await ctx.send(f"{tick} | Role {role.mention} has been renamed to {newname}")

    @role.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def color(self,ctx,role:discord.Role,color):
        ''' Changes the color of any role '''
        if role is None:
            return await ctx.send(f"{cross} | No role named {role} found in this server.")
        if not color.startswith("0x"):
            color = "0x"+color
        color = int(color,0)
        await role.edit(color=color)
        await ctx.send(f"{tick} | Role {role.mention}'s color has been changed to {color}")

    @commands.command()
    # @commands.bot_has_permissions(manage_roles=True)
    # @commands.has_permissions(manage_roles=True)
    async def inrole(self,ctx,*,role:discord.Role):
        ''' Gives the list of members having specified role '''
        role_name = role.name
        if role is None:
            return await ctx.send(f"{cross} No role named {role_name} found in this server.")
        member_list = []
        status_list = []
        for member in role.members:
            member1 = discord.utils.escape_markdown(str(member),as_needed=False,ignore_links=True)
            member_list.append(member1)
            status_list.append(member.status)
        # print(status_list)
        emoji_list = []
        for status in status_list:
            if "online" in status:
                emoji_list.append(online)
            elif "offline" in status or "invisible" in status:
                emoji_list.append(offline)
            elif "idle" in status:
                emoji_list.append(idle)
            elif "do_not_disturb" in status or "dnd" in status:
                emoji_list.append(dnd)
        if len(role.members) != 0:
            e = discord.Embed(
                description=" ",
                color=discord.Color.orange()
                )
            # e.add_field(name=f"Members with role {role} - [{len(role.members)}]",value="\n".join(f"{emote} | {name}" for emote,name in data_dict.items()))
            # TODO - Make the embed paginated to remove the error of max characters

            nums = len(emoji_list)
            pages = math.ceil(nums / 15)
            if nums <= 25:
                e.add_field(name=f"Members with role {role}",value="\n".join(f"`[{count+1}]` {emoji_list[count]} | {member_list[count]}" for count in range(0,len(emoji_list))))
                await ctx.send(embed=e)
            elif nums > 25:
                # LOGIC HERE -
                # for ex - 100 members in role 
                # pages = 100 / 25 = 4
                # 25 * 1 = 25, 25*2 = 50,25*3 = 75, 25*4 = 100
                # 25(I),26-50(II),51-75(III)
                # print(pages)
                page = [i for i in range(1,pages+1)]
                counts = []
                first_num = 0
                for i in page:
                    if first_num == 0:
                        last_num = (i*15) -1
                    else:
                        last_num = (i*15) -1
                    # last_num = (i*25) - 1
                    if first_num > len(emoji_list):
                        first_num = len(emoji_list)
                    elif last_num > len(emoji_list):
                        last_num = len(emoji_list)
                    l = [first_num,last_num]
                    counts.append(l)
                    if last_num == len(emoji_list) or first_num == len(emoji_list):
                        break
                    first_num = last_num + 1
                    
                # print(counts)
                # [[0,25],[26,50],[51,75]] # ---> FIRST LIST INDEX WILL NOT WORK
                # [[0,24],[25,50]]
                embeds = []
                for l in counts:
                    first_num = l[0]
                    last_num = l[1]
                    # print(first_num)
                    # print(last_num)
                    em = discord.Embed(description=" ",color=discord.Color.orange()).add_field(name=f"Members with role {role} - [{len(emoji_list)}]",value="\n".join(f"`[{count+1}]` {emoji_list[count]} | {member_list[count]}" for count in range(first_num,last_num)))
                    embeds.append(em)
                
                paginator = BotEmbedPaginator(ctx,embeds)
                await paginator.run()
            else:
                pass
        else:
            await ctx.send(f"There are no members with role {role_name}")


    # rainbow_role = ""

    # @role.command(pass_context=True)
    # @commands.has_permissions(manage_roles=True)
    # @commands.bot_has_permissions(manage_roles=True)
    # async def rainbow(self,ctx):
    #     global rainbow_role
    #     rainbow_role = await ctx.guild.create_role(name="Rainbow",color=discord.Color.random())
    #     self.rainbow_task.start()
    
    # @tasks.loop(seconds=20)
    # async def rainbow_task(self):
    #     global rainbow_role
    #     await rainbow_role.edit(color=discord.Color.random())
    

    # color_list = [0xFFFFFF,0x1ABC9C,0x2ECC71,0x3498DB,0x9B59B6,0xE91E63,0xF1C40F,0xE67E22,0xE74C3C,0x34495E,0x11806A,0x1F8B4C,0x206694,0x71368A,0xAD1457,0xC27C0E,0xA84300,0x992D22,0x2C3E50]
    # @role.command()


def setup(bot):
    bot.add_cog(Role(bot))
    print(OKGREEN+"[STATUS OK] Role cog is ready!")