import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

# Set up bot with command prefix and intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='/', intents=intents)
allowed_mentions = discord.AllowedMentions(users=True, roles=True, everyone=True)
bot.allowed_mentions = allowed_mentions

class CraftView(discord.ui.View):
    def __init__(self, original_creator):
        super().__init__(timeout=None)  # No timeout so the buttons stay indefinitely
        self.locked = False
        self.done = False
        self.locking_user = None
        self.original_creator = original_creator

    @discord.ui.button(label="Lock", style=discord.ButtonStyle.blurple, custom_id="lock_button", emoji="🔒")
    async def lock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.done:
            await interaction.response.send_message(
                f"This crafting order has already been completet by {self.locking_user.display_name}",
                ephemeral=True
            )
            return
        if self.locked:
            await interaction.response.send_message(
                f"This crafting order has already been locked by {self.locking_user.display_name}",
                ephemeral=True
            )
            return
        else:
            self.locked = True
            self.locking_user = interaction.user
            embed = interaction.message.embeds[0].to_dict()
            new_embed = discord.Embed.from_dict(embed)
            new_embed.color = discord.Color.blue()
            await interaction.response.edit_message(
                content=f"🔒 Crafting order is locked by {self.locking_user.display_name}!",
                embed=new_embed,
                view=self
            )

    @discord.ui.button(label="Unlock", style=discord.ButtonStyle.secondary, custom_id="unlock_button", emoji="🔓")
    async def unlock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.done:
            await interaction.response.send_message(
                f"This crafting order has already been completet by {self.locking_user.display_name}",
                ephemeral=True
            )
            return
        if interaction.user != self.locking_user:
            await interaction.response.send_message(
                "You are not authorized to unlock this crafting order.",
                ephemeral=True
            )
            return

        if not self.locked:
            await interaction.response.send_message(
                "This crafting order is not locked.",
                ephemeral=True
            )
            return
        
        # Reset the form but keep the supplied information
        self.locked = False
        self.locking_user = None
        embed = interaction.message.embeds[0].to_dict()
        new_embed = discord.Embed.from_dict(embed)
        new_embed.color = discord.Color.yellow()
        
        await interaction.response.edit_message(
            content="🔓 This crafting order has been unlocked!",
            embed=new_embed,
            view=self  # Keep the buttons so the form can be locked again
        )

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green, custom_id="done_button", emoji="✅")
    async def done_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.done:
            await interaction.response.send_message(
                f"This crafting order has already been completet by {self.locking_user.display_name}",
                ephemeral=True
            )
            return
        if interaction.user == self.locking_user:
            self.done = True
            embed = interaction.message.embeds[0].to_dict()
            new_embed = discord.Embed.from_dict(embed)
            new_embed.color = discord.Color.green()  # Change color to indicate it's done

            await interaction.response.edit_message(
                content=f"✅ Crafting Order Completed by {interaction.user.display_name}, {self.original_creator.mention}",
                embed=new_embed,
                view=self,
                allowed_mentions=allowed_mentions,
            )
        else:
            await interaction.response.send_message(
                "You are not authorized to mark this crafting order as 'Done'.",
                ephemeral=True
            )
    
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red, custom_id="delete_button", emoji="🗑️")
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.original_creator:
            await interaction.response.send_message(
                "You are not authorized to delete this crafting order.",
                ephemeral=True
            )
            return

        # Delete the message
        await interaction.message.delete()

def create_form_embed():
    embed = discord.Embed(
        title="Crafting Order",
        description="Fill out the crafting order by providing the following details:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Item Name", value="Provide the name of the item you want to craft.", inline=False)
    embed.add_field(name="Materials Needed", value="List all materials needed, with ranks.", inline=False)
    embed.add_field(name="Optional Crafting Reagents", value="Provide all optional crafting reagents (if any, otherwise write 'none').", inline=False)
    embed.add_field(name="Minimum Rank", value="Provide minimum rank (if any, otherwise write 'none').", inline=False)
    embed.add_field(name="Profession Needed", value="Provide the needed profession for the craft.", inline=False)
    
    return embed

# This is how you register a slash command
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    guild = discord.Object(GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=guild)  # Sync the slash commands with the Discord API
        print(f"Synced {len(synced)} command(s) to the guild {guild.id}.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Registering the slash command using app_commands
@bot.tree.command(name="craft", description="Creates a new crafting order")
async def create_crafting_order(interaction: discord.Interaction):
    try:
        # Defer the interaction to avoid timeout
        await interaction.response.defer()

        dm_channel = await interaction.user.create_dm()

        # Always send the form embed
        await dm_channel.send(embed=create_form_embed())

        # Wait for user input
        await dm_channel.send("Item name:")
        item_name_msg = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == dm_channel)

        await dm_channel.send("Materials needed, with ranks:")
        materials_msg = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == dm_channel)

        await dm_channel.send("Optional crafting reagents (if any, otherwise write 'none'):")
        optional_crafting_reagents_msg = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == dm_channel)

        await dm_channel.send("Minimum crafted rank (if any, otherwise write 'none'):")
        crafting_time_msg = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == dm_channel)

        await dm_channel.send("Profession needed for the craft:")
        needed_prof_msg = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == dm_channel)

        # Creating the response embed
        response_embed = discord.Embed(
            title=f"Crafting order from {interaction.user.display_name}",
            color=discord.Color.yellow()
        )
        response_embed.add_field(name="Item Name", value=item_name_msg.content, inline=False)
        response_embed.add_field(name="Profession Needed", value=needed_prof_msg.content, inline=False)
        response_embed.add_field(name="Materials Needed", value=materials_msg.content, inline=True)
        response_embed.add_field(name="Optional Reagents", value=optional_crafting_reagents_msg.content or "None", inline=True)
        response_embed.add_field(name="Minimum Rank", value=crafting_time_msg.content or "None", inline=False)

        view = CraftView(interaction.user)
        # Send the final response after all input is gathered
        await interaction.followup.send(content=":unlock: A new crafting order has been created!", embed=response_embed, view=view)

        await dm_channel.send(f"You're order has successfully been created in {interaction.channel}")

    except discord.Forbidden:
        await interaction.response.send_message(f"I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred. DM @Shibabo with the following error: {e}")

# Run the bot with your token
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print("Failed to start bot: " + str(e))
