import discord
import os
from discord import app_commands
from discord.ext import commands
import requests
from datetime import datetime, timezone
from ApWebAPI import ArchipelagoAPI
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
APWEB = os.getenv('APHOST')

# Bot setup
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

def get_patch_for_slot(slot_number, slot_patch):
    patch = slot_patch.get(slot_number)
    if patch is None:
        return "None"
    return f"{APWEB}{patch}"

def room_embed(room_id: str) -> discord.Embed:
    data = ArchipelagoAPI(APWEB).get_room_status(room_id)

    room_url = f"{APWEB}/room/{room_id}"
    tracker_url = f"{APWEB}/tracker/{data['tracker']}"

    # Room info
    embed = discord.Embed(
        title="Archipelago Room Status",
        url=room_url,
        color=0x30a2ff,
    )

    embed.add_field(name="Room ID", value=f"{room_id}", inline=True)
    embed.add_field(name="Port", value=f"**{data['last_port']}**", inline=True)
    embed.add_field(name="Tracker", value=f"[View Tracker]({tracker_url})", inline=False)
    
    # Players list
    players = data.get("players", [])
    downloads = data.get("downloads", [])
    slot_patches = {item['slot']: item['download'] for item in downloads}
    #print(players)
    print(slot_patches)
    if players:
        lines = [
            #f"{i+1}. **{name}** — *{game}* - {patch if (patch := get_patch_for_slot(i+1, slot_patches)) != 'None' else 'No Patch'}"
            f"{i+1}. **{name}** - __{game}__: {f'[Download Patch]({patch})' if (patch := get_patch_for_slot(i+1, slot_patches)) != 'None' else 'No Patch'}"
            for i, (name, game) in enumerate(players)
            ]
        # stay under 1000 characters    
        chunk, chunks = "", []
        for line in lines:
            if len(chunk) + len(line) + 1 > 1000:
                chunks.append(chunk)
                chunk = line
            else:
                chunk = f"{chunk}\n{line}" if chunk else line
        if chunk:
            chunks.append(chunk)

        # Adds to Embed
        for index, c in enumerate(chunks):
            label = f"Players ({len(players)})" if index == 0 else "Players (cont.)"
            embed.add_field(name=label, value=c, inline=False)

    embed.add_field(name="Last Activity", value=data.get("last_activity", "Unknown"), inline=True)
    return embed

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# Default room (resets on restart) save to file later verify room exisit before saving for security reasons
default_rooms: dict[int, str] = {}

# Room Status
@bot.tree.command(name="room", description="Show the status of an Archipelago room")
@app_commands.describe(room_id="The room SUUID (leave blank to use the server default)")
async def room_cmd(interaction: discord.Interaction, room_id: str = None):
    await interaction.response.defer()

    rid = room_id or default_rooms.get(interaction.guild_id)
    if not rid:
        await interaction.followup.send(
            "No room ID provided and no default set.\n"
            "Use `/room <room_id>` or `/setroomid <room_id>`.",
            ephemeral=True,
        )
        return

    try:
        embed = room_embed(rid)
        await interaction.followup.send(embed=embed)
    except requests.HTTPError as e:
        await interaction.followup.send(
            f"Room not found or the server returned an error.\n`{e}`",
            ephemeral=True,
        )
    except requests.ConnectionError:
        await interaction.followup.send(
            "Could not reach " + APWEB + ".",
            ephemeral=True,
        )

# Set Room ID - add to file later
@bot.tree.command(name="setroomid", description="Set a default room ID for this server.")
@app_commands.describe(room_id="The room SUUID to use as the default")
async def set_room_cmd(interaction: discord.Interaction, room_id: str):
    default_rooms[interaction.guild_id] = room_id
    await interaction.response.send_message(
        f"Default room set to `{room_id}`.\nYou can now run `/room` without specifying an ID.",
        ephemeral=True,
    )

bot.run(BOT_TOKEN)