import discord

from pterobot import settings

class PteroBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

client = PteroBot()
settings = settings.PterobotSettings()
client.run(settings.token)