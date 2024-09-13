import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot with command prefix and intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='/', intents=intents)

class CraftView(discord.ui.View):
    def __init__(self, locked_user):
        super().__init__(timeout=None)  # No timeout so the buttons stay indefinitely
        self.locked_user = locked_user
        self.locked = False

    @discord.ui.button(label="Lock", style=discord.ButtonStyle.blurple, custom_id="lock_button")
    async def lock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.locked:
            await interaction.response.send_message(
                "This form is already locked.",
                ephemeral=True
            )
            return

        if interaction.user != self.locked_user:
            await interaction.response.send_message(
                "You are not authorized to lock this form.",
                ephemeral=True
            )
            return
        
        self.locked = True
        await interaction.response.edit_message(
            content=f"This form is now locked by {self.locked_user.display_name}",
            view=self
        )

    @discord.ui.button(label="Unlock", style=discord.ButtonStyle.red, custom_id="unlock_button")
    async def unlock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.locked_user:
            await interaction.response.send_message(
                "You are not authorized to unlock this form.",
                ephemeral=True
            )
            return

        if not self.locked:
            await interaction.response.send_message(
                "This form is not locked.",
                ephemeral=True
            )
            return
        
        # Reset the form but keep the supplied information
        self.locked = False
        embed = interaction.message.embeds[0].to_dict()
        embed['footer']['text'] = "This response is unlocked and can be locked again."
        new_embed = discord.Embed.from_dict(embed)

        await interaction.response.edit_message(
            content="This form has been reset and can be locked again.",
            embed=new_embed,
            view=self  # Keep the buttons so the form can be locked again
        )
        await interaction.followup.send("Craft form has been reset.", ephemeral=True)


def create_form_embed():
    embed = discord.Embed(
        title="Crafting Order",
        description="Fill out the crafting order by providing the following details:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Item Name", value="Provide the name of the item you want to craft.", inline=False)
    embed.add_field(name="Materials Needed", value="List all materials needed, with ranks.", inline=False)
    embed.add_field(name="Optional Crafting Reagents", value="Provide all optional crafting reagents (if any), otherwise leave empty.", inline=False)
    embed.add_field(name="Minimum Rank", value="Provide minimum rank (if any), otherwise leave empty.", inline=False)
    embed.add_field(name="Profession Needed", value="Provide the needed profession for the craft.", inline=False)
    
    return embed

@bot.command(name='craft')
async def craft_command(ctx):
    try:
        dm_channel = await ctx.author.create_dm()
        
        # Always send the form embed
        await dm_channel.send(embed=create_form_embed())

        # Wait for user input
        await dm_channel.send("Item name:")
        item_name_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel)

        await dm_channel.send("Materials needed, with ranks:")
        materials_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel)

        await dm_channel.send("Optional crafting reagents (if any, otherwise write 'none'):")
        optional_crafting_reagents_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel)

        await dm_channel.send("Minimum crafted rank (if any, otherwise write 'none'):")
        crafting_time_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel)

        await dm_channel.send("Profession needed for the craft:")
        needed_prof_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel)

        # Creating the response embed
        response_embed = discord.Embed(
            title=f"Craft Form for {ctx.author.display_name}",
            color=discord.Color.green()
        )
        response_embed.add_field(name="Item Name", value=item_name_msg.content, inline=False)
        response_embed.add_field(name="Profession Needed", value=needed_prof_msg.content, inline=False)
        response_embed.add_field(name="Materials Needed", value=materials_msg.content, inline=True)
        response_embed.add_field(name="Optional Reagents", value=optional_crafting_reagents_msg.content or "None", inline=True)
        response_embed.add_field(name="Minimum Rank", value=crafting_time_msg.content or "None", inline=False)

        view = CraftView(locked_user=ctx.author)
        await ctx.send(embed=response_embed, view=view)

    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, I couldn't send you a DM. Please check your DM settings.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


# Run the bot with your token
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print("Failed to start bot: " + str(e))
