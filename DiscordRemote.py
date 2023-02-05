import discord
import json
import sys
from sys import platform
import textwrap
import subprocess
import os

print("Loading Discord Client...")

TOKEN = "";#Enter your bot token here
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
guilds = []
showChat = False;

print("Loading JSONs...")
adminsjson = open("admins.json", "r", encoding="utf-8")
admins = json.load(adminsjson)
adminsjson.close()
print("Loaded JSON's!\nSucessfully Loaded Discord Client!\nStarting Discord Client...")

async def messages(message, user_message, userid):
    if str(userid) in admins["admins"]:
        command = user_message[1:len(user_message)];
        #Bot Commands
        if user_message[0] == '!':
            if command == "help":
                await message.channel.send(f"Hello! I'm a remote control bot! The host machine that I am running is running {platform}!\n\nCommands:\n-addadmin: Add's an admin\n-removeadmin: Remove's an admin")
            elif command[0:8] == "addadmin":
                admin = command[9:len(command)]
                if not admin in admins["admins"]:
                    admins["admins"].append(admin)
                    json = open("admins.json", "w", encoding="utf-8")
                    json.dump(admins, json)
                    json.close()
                else:
                    await message.channel.send("Sorry but that user is already an admin!")
            elif command[0:11] == "removeadmin":
                admin = command[12:len(command)]
                if admin in admins["admins"]:
                    admins["admins"].remove(admin)
                    json = open("admins.json", "w", encoding="utf-8")
                    json.dump(admins, json)
                    json.close()
                else:
                    await message.channel.send("Sorry but that user isn't an admin!")
        #Computer Remote Control commands
        elif user_message[0] == '$':
            print(f"{message.author}/{userid} ENTERED THE COMMAND {command}\nOUTPUT:")
            try:
                os.system(command)
            except Exception as error:
                await message.channel.send(str(error))
            print("END OF COMMAND")
            for outputline in textwrap.wrap(subprocess.getoutput(command), 2000):
                await message.channel.send(outputline)

@client.event
async def on_ready():
    print("Client Started!\nLoading Server List...")
    print("SERVERS:\n--------")
    for guild in client.guilds:
        print(str(guild.name) + ': \n' + "ID: " + str(guild.id) + ", " + "COUNT: " + str(guild.member_count) + '\n')
        guilds.append(guild)
    print("Loaded Server List!\nWe have logged in as {0.user}!".format(client))
    
@client.event
async def on_message(message):
    userid = int(message.author.id)
    user_message = str(message.content)
    
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        if showChat:
            print(f"TYPE: directChat ID: {str(userid)} NAME: {str(message.author)} MESSAGE: {user_message}")
        await messages(message, user_message, userid)
    else:
        if showChat:
            print(f"TYPE: server SERVER: {message.guild.name}/{message.guild.name.id} CHANNEL: {message.channel.name}/{message.channel.name.id} ID: {str(userid)} NAME: {str(message.author)} MESSAGE: {user_message}")
        channel = str(message.channel.name)
        if message.channel.name == channel:
            await messages(message, user_message, userid)
            
client.run(TOKEN)
