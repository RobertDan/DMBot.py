# bot.py
import os
import time

import discord
from command_processing import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    #Build folder structure
    try:
        os.makedirs('data')
    except OSError as e:
        #print("Folder \"data\" already exists.")
        ""

        
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[:1] != "!":
        return

    print(message.author, ":", message.content)

    #logic to determine what code to run
    if message.content[:11] == "!rollcustom":
        response = process_command_rollcustom(message)
    elif message.content[:5] == "!roll":
        response = process_command_roll(message)
    elif message.content[:11] == "!savecustom":
        response = process_command_savecustom(message)
    elif message.content[:6] == "!stats":
        response = process_command_stats(message)
    elif message.content[:9] == "!loadchar":
        response = process_command_loadchar(message)
    elif message.content[:8] == "!addstat":
        response = process_command_addstats(message)
    elif message.content[:11] == "!removestat":
        response = process_command_removestats(message)
    elif message.content[:5] == "!help":
        response = process_command_help(message)
    else:
        return
    
    await message.channel.send(response)
    return

try:
    client.run(TOKEN)
except:
    print("error happened at: " + time.strftime('%X %x'))
