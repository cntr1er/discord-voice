import os
import threading
import discord
from discord.ext import commands
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import json

# Bot configuration
prefix = ','
bot = commands.Bot(command_prefix=prefix,
                   help_command=None,
                   case_insensitive=True,
                   self_bot=True)

voice_channel = None
is_connected = False

# Load configuration from config.json
with open('config.json') as f:
    config = json.load(f)

token = config["token"]
voice_channel_id = config["voice_channel_id"]

@bot.event
async def on_ready():
    global voice_channel, is_connected

    print(f'Logged in as {bot.user}')

@bot.command()
async def start(ctx):
    global is_connected, voice_channel, voice_client

    voice_channel = bot.get_channel(voice_channel_id)

    if not is_connected:
        if voice_channel:
            try:
                voice_client = await voice_channel.connect()
                is_connected = True
                await ctx.send(f'Connected to {voice_channel.name}.')
                print(f'Connected to {voice_channel.name}.')
            except Exception as e:
                await ctx.send(f'Error connecting to the voice channel: {e}')
                print(f'Error connecting to the voice channel: {e}')
        else:
            await ctx.send(f'Failed to find the voice channel with ID {voice_channel_id}.')
    else:
        await ctx.send(f'Already connected to {voice_channel.name}.')




# Function to create an icon for the system tray
def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill="blue")
    return image


# Function to stop the bot from the system tray
def stop_bot(icon, item):
    icon.stop()  # Stop the tray icon
    os._exit(0)  # Forcefully stop the script


# System tray setup
def setup_tray():
    icon = Icon(
        "Discord Bot",
        create_image(),
        menu=Menu(MenuItem("Exit", stop_bot))
    )
    icon.run()


# Run the bot
def run_bot():
    bot.run(token, bot=False)


# Start the bot and tray icon
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    setup_tray()

