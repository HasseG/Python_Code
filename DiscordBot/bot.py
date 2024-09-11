import discord
import response
from discord.ext import commands
import os
from dotenv import load_dotenv

async def send_message(message, user_message, is_private):
    
    try:
        handledMessage = response.handle_response(user_message)
        if handledMessage == "It is good to see you again, ":
            newResponse = handledMessage + message.author.mention
            print(newResponse)
            
            await message.author.send(newResponse) if is_private else await message.channel.send(newResponse)
        else:
            await message.author.send(handledMessage) if is_private else await message.channel.send(handledMessage)
    except Exception as e:
        print(e)
        
        
def rund_discord_bot():
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    client = discord.Client(intents=discord.Intents.all())
    @client.event
    async def on_ready():
        print(f"{client.user} is now running")
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f"{username} said: '{user_message}' ({channel})")
        
        
        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else: 
            await send_message(message, user_message, is_private=False)
        
    client.run(DISCORD_TOKEN)