import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import array

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("There's a full moon tonight!")

@bot.event
async def on_message(message):
    if "```" in message.content.lower():
        pins = await message.channel.pins()
        if len(pins) >= 50:
            for pin in pins:
                if "vote" in pin.content.lower():
                    pin.unpin()
                    break
        await message.pin(reason=None)
    await bot.process_commands(message)

@bot.command()
async def create(ctx, *, arg):
    print(arg)

    currentGameCategory = discord.utils.get(ctx.guild.categories, name="CURRENT GAME")
    archiveCategory = discord.utils.get(ctx.guild.categories, name = "ARCHIVED GAMES S4 8-10")

    currentGameChannels = currentGameCategory.channels

    if len(currentGameChannels) > 0:
        for channel in currentGameChannels:
            await channel.edit(category=archiveCategory)

    dayChannel = await ctx.guild.create_text_channel(f'{arg}-day-chat')
    nightChannel = await ctx.guild.create_text_channel(f'{arg}-night-chat')
    heavenChannel = await ctx.guild.create_text_channel('heaven-chat')
    wolfChannel = await ctx.guild.create_text_channel('wolf-chat')

    await dayChannel.edit(category=currentGameCategory)
    await nightChannel.edit(category=currentGameCategory)
    await heavenChannel.edit(category=currentGameCategory)
    await wolfChannel.edit(category=currentGameCategory)

@bot.command()
async def roll(ctx, *, arg): #Output a random user given the role
    roleName = arg
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    
    if role is None:
        await ctx.send("I can't find that role, sorry!")
        return
    empty = True
    players = []
    for member in ctx.guild.members:
        if role in member.roles:
            players.append(member.name)
            empty = False
    if empty:
        await ctx.send("Looks like there aren't any wolves out tonight.")
    else:
        chosen = random.choice(players)
        await ctx.send(f'{chosen}')


bot.run(TOKEN)