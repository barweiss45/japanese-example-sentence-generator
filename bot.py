import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('discord_api_key')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return


client = MyClient()
client.run('TOKEN')
