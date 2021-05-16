import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class Chatbot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.chatbot = ChatBot("The Coderz Bot")
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train("chatterbot.corpus.english")
        trainer.train("chatterbot.corpus.english.greetings")
        trainer.train("chatterbot.corpus.english.conversations")

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def chatbot(self,ctx):
        pass

    def get_chat_ready(self):
        return True

    @commands.Cog.listener()
    async def on_message(self,message):
        # flag,chatbot = get_chat_ready()
        # print(message.author)
        if message.author.name == "The Coderz Bot":
            pass
        else:
            resp = self.chatbot.get_response(message.content)
            await message.channel.send(resp)


def setup(bot):
    bot.add_cog(Chatbot(bot))
    print("chatbot is ready")