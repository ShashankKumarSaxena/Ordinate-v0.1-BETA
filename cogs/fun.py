import discord
from discord.ext import commands
from cogs.utils.color import fetch_color
from colorama import init, Fore
import asyncio
from cogs.utils.emoji import tick,qtick,cross,qcross
import random

init(autoreset=True)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx):
        ''' Play rock paper scissors with bot '''
        em = discord.Embed(
            title="Rock Paper Scissor",
            color=await fetch_color(bot=self.bot, ctx=ctx),
            description=f"Choose any option from by reacting!\n\n"
                        + f":fist: Rock\n\n"
                        + f":raised_hand: Paper\n\n"
                        + f":scissors: Scissor"
        )
        msg = await ctx.send(embed=em)
        fist = "✊"
        hand = "✋"
        scissor = "✂"
        choice_list = [fist,hand,scissor]
        await msg.add_reaction("✊")
        await msg.add_reaction("✋")
        await msg.add_reaction("✂")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in choice_list

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{cross} | Time up!")
        else:
            bot_choice = random.choice(choice_list)

            emb = discord.Embed(title="Rock Paper Scissor",
                                color=await fetch_color(bot=self.bot,ctx=ctx))

            if reaction is not None:
                if bot_choice == fist and reaction.emoji == fist:
                    emb.description = f"You choose {fist} and bot choose {fist}"
                    emb.add_field(name="Result",value="Tie")
                    await msg.edit(embed=emb)
                elif bot_choice == fist and reaction.emoji == hand:
                    emb.description = f"You choose {hand} and bot choose {fist}"
                    emb.add_field(name="Result",value="You won!")
                    await msg.edit(embed=emb)
                elif bot_choice == fist and reaction.emoji == scissor:
                    emb.description = f"You choose {scissor} and bot choose {fist}"
                    emb.add_field(name="Result",value="Bot won")
                    await msg.edit(embed=emb)
                elif bot_choice == hand and reaction.emoji == fist:
                    emb.description = f"You choose {fist} and bot choose {hand}"
                    emb.add_field(name="Result",value="Bot won")
                    await msg.edit(embed=emb)
                elif bot_choice == hand and reaction.emoji == hand:
                    emb.description = f"You choose {hand} and bot choose {hand}"
                    emb.add_field(name="Result",value="Tie")
                    await msg.edit(embed=emb)
                elif bot_choice == hand and reaction.emoji == scissor:
                    emb.description = f"You choose {scissor} and bot choose {hand}"
                    emb.add_field(name="Result",value="You won!")
                    await msg.edit(embed=emb)
                elif bot_choice == scissor and reaction.emoji == fist:
                    emb.description = f"You choose {fist} and bot choose  {scissor}"
                    emb.add_field(name="Result",value="You won!")
                    await msg.edit(embed=emb)
                elif bot_choice == scissor and reaction.emoji == hand:
                    emb.description = f"You choose {hand} and bot choose  {scissor}"
                    emb.add_field(name="Result",value="Bot won")
                    await msg.edit(embed=emb)
                elif bot_choice == scissor and reaction.emoji == scissor:
                    emb.description = f"You choose {scissor} and bot choose  {scissor}"
                    emb.add_field(name="Result",value="Tie")
                    await msg.edit(embed=emb)


# TicTacToe soon :)

def setup(bot):
    bot.add_cog(Fun(bot))
    print(Fore.GREEN+"[STATUS OK] Fun cog is ready!")
