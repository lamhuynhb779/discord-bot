from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime

BOT_TOKEN = "MTA4MTU5NjYwODQ1MTQ0ODg2Mg.GnruXm.QdcfVR4RBUjf4XwKIMyliXvYh7k23X3vbhnyq0"
CHANNEL_ID = 1081607559934382141
MAX_SESSION_TIME_MINUTES = 1

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0
    end_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

session = Session()

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    # Ignore the first execution of this command
    if break_reminder.current_loop == 0:
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")

@bot.event
async def on_ready():
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

@bot.command()
async def hello(context):
    await context.send("Hello!")

@bot.command()
async def add(context, param1, param2):
    result = int(param1) + int(param2)
    await context.send(f"{param1} + {param2} = {result}")

@bot.command()
async def addmore(context, *params):
    result = 0
    for param in params:
        result += int(param)
    await context.send(f"Result = {result}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
      
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    break_reminder.start()

    await ctx.send(f"New session started at {human_readable_time}.")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
      
    session.is_active = False
    session.end_time = ctx.message.created_at.timestamp()
    duration = session.end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()

    await ctx.send(f"Session ended after {human_readable_duration} seconds.") 

bot.run(BOT_TOKEN)
