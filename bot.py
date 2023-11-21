import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

response = requests.get('https://oxylabs.io/')

GPTclient = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}! I\'m GuildPT!')

    if message.content == 'bye':
        await message.channel.send(f'Goodbye and goodnight, {message.author}')

    await bot.process_commands(message)

@bot.command()
async def square(ctx, arg):
    print(arg)

    if(arg.isnumeric()):
        await ctx.send(int(arg) ** 2)
    else:
        await ctx.send('Sorry, I can only square numbers!')

@bot.command()
async def timestamp(ctx, arg):
    print(ctx.author)

@bot.command() #No GPT cause money. :( 
async def GPT(ctx, arg):
    print(ctx.author)

@bot.command()
async def request(ctx, arg):
    argResponse = requests.get(f'{arg}')
    soup = BeautifulSoup(argResponse.text, 'html.parser')
    await ctx.send(soup.title)
    

bot.run(TOKEN)
