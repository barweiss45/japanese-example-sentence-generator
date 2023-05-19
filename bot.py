import os
import discord
from langchain.llms import OpenAI
from discord.ext import commands
from forvo_api import get_pronounciation
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.getenv('discord_api_key')
openai_api_key = os.getenv('openai_api_key')

llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event    
async def on_ready():
    guild = discord.utils.get(bot.guilds)
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} is active in {guild.id}')
    
@bot.command(name='ping')
async def on_message(ctx):
    await ctx.send('pong')
    
@bot.command(name='llm')
async def on_message(ctx, arg):
    llm_output = llm(arg)
    print(f"{ctx.author}Sent: {ctx.message}\n\nLLM Sent: {llm_output}")
    await ctx.send(llm_output)

bot.run(TOKEN)
