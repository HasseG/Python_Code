import discord
import response

async def send_message(message, user_message, is_private):
    
    
    try:
        response1 = response.handle_response(user_message)
        if response1 == "It is good to see you again, ":
            reponse_message = response1 + str(message.member.user.globalName)
            
            print(reponse_message)
            
            await message.author.send(reponse_message) if is_private else await message.channel.send(reponse_message)
        else:
            await message.author.send(reponse_message) if is_private else await message.channel.send(reponse_message)
    
    except Exception as e:
        print(e)
        
        
def rund_discord_bot():
    TOKEN = ""
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
            await send_message(message, user_message,is_private=False)
        
    client.run(TOKEN)