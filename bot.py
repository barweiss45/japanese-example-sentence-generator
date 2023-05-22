import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from ai_api import query_to_llm
import tests

load_dotenv('.env')

TOKEN = os.environ['DISCORD_API_KEY']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event    
async def on_ready():
    guild = discord.utils.get(bot.guilds)
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} is active in {guild.id}')
    
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command(name='sentence')
async def sentence(ctx, arg):
    if tests.is_japanese(arg) == True:
        llm_output = query_to_llm(arg)
        await ctx.send(llm_output)
    else:
        await ctx.send("There was an issue with your input. Use Japanese characters only.")

bot.run(TOKEN)
