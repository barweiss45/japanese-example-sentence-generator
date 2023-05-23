import os
import logging
import discord
import requests
import tests
from discord.ext import commands
from dotenv import load_dotenv
from ai_api import query_to_llm
from bot_http_api_auth import get_token, BASE_URL
from forvo_api import get_pronounciation

# Set up logging
discord.utils.setup_logging(level=logging.DEBUG)

load_dotenv()

TOKEN = os.environ['DISCORD_BOT_TOKEN']
BEARER_TOKEN = get_token()
headers = {
      'Authorization': f'Bearer {BEARER_TOKEN}',
  }

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')
# embed = discord.Embed()

@bot.event    
async def on_ready():
    guild = discord.utils.get(bot.guilds)
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} is active in {guild.id}')
    
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='channel')
async def channel(ctx):
    r = requests.get(f"{BASE_URL}/channel/id", headers=headers)
    await ctx.send(r.json())

async def get_sentence(arg):
    if tests.is_japanese(arg) == True:
        return query_to_llm(arg)
    else:
        logging.error(f'A message failed for is_japanese test. {arg} was entered.')
        return("There was an issue with your input. Use Japanese characters only.")
        
@bot.command(name='sentence')
async def sentence(ctx, arg): #
    async with ctx.typing():
        msg = await get_sentence(arg)
        logging.debug(msg)
    await ctx.send(msg)

bot.run(TOKEN)
