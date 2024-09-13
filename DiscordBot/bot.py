import discord
import response
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

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

async def create_form_embed():
    embed = discord.Embed(
        title="Craft Form",
        description="Fill out the form by providing the following details:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Item Name", value="Type the name of the item you want to craft.", inline=False)
    embed.add_field(name="Materials Needed", value="List all materials needed.", inline=False)
    embed.add_field(name="Crafting Time", value="Specify the time needed to craft.", inline=False)
    embed.set_footer(text="React with 🔒 to lock this form to yourself.")
    return embed

async def collect_form_data(ctx, client):
    def check_author(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        await ctx.channel.send("Please provide the item name:")
        item_name_msg = await client.wait_for("message", check=check_author, timeout=60)
        await ctx.send("Please provide the materials needed:")
        materials_msg = await client.wait_for("message", check=check_author, timeout=60)
        await ctx.send("Please provide the crafting time:")
        crafting_time_msg = await client.wait_for("message", check=check_author, timeout=60)

        response_embed = discord.Embed(
            title=f"Craft Form for {ctx.author.display_name}",
            color=discord.Color.green()
        )
        response_embed.add_field(name="Item Name", value=item_name_msg.content, inline=False)
        response_embed.add_field(name="Materials Needed", value=materials_msg.content, inline=False)
        response_embed.add_field(name="Crafting Time", value=crafting_time_msg.content, inline=False)
        response_embed.set_footer(text="This response is locked to the user who reacts.")

        response_message = await ctx.send(embed=response_embed)
        await response_message.add_reaction("🔒")

        def check_reaction(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) == "🔒"
                and reaction.message.id == response_message.id
            )

        await client.wait_for("reaction_add", check=check_reaction, timeout=30)
        await response_message.edit(embed=response_embed.set_footer(text=f"Locked by {ctx.author.display_name}"))

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")

def run_discord_bot():
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

        if user_message.startswith("/craft"):
            form_embed = await create_form_embed()
            form_message = await message.channel.send(embed=form_embed)
            await form_message.add_reaction("🔒")

            # Collect form data
            await collect_form_data(message, client)

        elif user_message.startswith("?"):
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(DISCORD_TOKEN)

# Start the bot
run_discord_bot()
