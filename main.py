import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import subprocess
import platform
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Create a lock
bot_lock = asyncio.Lock()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

if platform.system() == "Windows":
    SCRIPT_PATH = '..\Carleton-Library-Autobooking\Autobook.py'
else:
    SCRIPT_PATH = '../Carleton-Library-Autobooking/Autobook.py'

@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))

    # Sync all application commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    print('Bot is ready')

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the command if it's for all guilds.
@bot.tree.command(
    name='help',
    description='Prints the usage'
)
async def help(
    interaction: discord.Interaction
):
    message = '''This bot books Carleton Library rooms
                It's ran on a Pi 3 - Model A+ so it will take
                about a minute to run.
                Script @ https://github.com/HenryZhangxiao/Carleton-Library-Autobooking
                Bot @ https://github.com/HenryZhangxiao/Carleton-Library-Autobooking-Bot'''
    await interaction.response.send_message(message, ephemeral=True)

@bot.tree.command(
    name='book',
    description='Book a library room'
)
@app_commands.describe(
    username="Your Carleton Central username",
    password="Your Carleton Central password",
    day="Day you want to book for",  # Day to book
    room="The room you want to book for",  # Room to book
    time="The start time of your booking in military hours",  # Booking start time
    duration="Duration of your booking in 30 minute increments (Default 180)"  # Optional duration for the booking
)
async def book(
    interaction: discord.Interaction,
    username: str,  # Carleton Central username
    password: str,  # Carleton Central password
    day: str,  # Day to book
    room: str,  # Room to book
    time: str,  # Booking start time
    duration: str = "180"  # Optional duration for the booking
):
    # Acquire the lock
    async with bot_lock:
        try:
            await interaction.response.defer()
            # Build the command-line arguments for the script
            if platform.system() == "Windows":
                command = ["python", SCRIPT_PATH, 
                        "-u", username, 
                        "-p", password, 
                        "-d", day, 
                        "-r", room, 
                        "-t", time, 
                        "--duration", duration, 
                        "--headless"
                        ]
                # command = ["python", SCRIPT_PATH, '-h']
            else:
                command = ["python3", SCRIPT_PATH, 
                        "-u", username, 
                        "-p", password, 
                        "-d", day, 
                        "-r", room, 
                        "-t", time, 
                        "--duration", duration, 
                        "--headless", 
                        "--rpi"
                        ]
            
            print(f"Resolved script path: {SCRIPT_PATH}")
            
            # Run the script and capture its output
            result  = subprocess.run(command, text=True, capture_output=True)
            return_code = result.returncode

            # Send message based on return_code from script
            match return_code:
                case 0:  # SUCCESS
                    message = f"Library room booked successfully"
                case 1:  # ERROR
                    message = f"Undefined error booking the room"
                case 2:  # ERR_INVALID_ROOM 
                    message = f"Invalid room selected"
                case 3:  # ERR_NO_CREDENTIALS
                    message = f"No login credentials provided"
                case 4:  # ERR_MONTH_MANUPULATION
                    message = f"Month manipulation failed"
                case 5:  # ERR_UNIX_TIMESTAMP
                    message = f"Failed getting unix timestamp"
                case 6:  # ERR_CARLETON_LOGIN
                    message = f"Failed to login to Carleton Central"
                case 7:  # ERR_BOOK_ROOM
                    message = f"Failed to book room"
                case 8:  # ERR_DISCORD_POST
                    message = f"The room booking was successful\n"
                    message += f"Failed to post to Discord"
                case _:  # Catchall
                    message = f"Unhandled error booking the room"
            await interaction.followup.send(message)

        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

bot.run(TOKEN)
