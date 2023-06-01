from discord import Client
from asyncio import sleep
from discord.ext import tasks

guild_ids = [00000000] # Only servers where the commands will work in (safety feature). Example: [000000000, 000002311, 123689923]. Use https://support.discord.com/hc/articles/206346498 to find ids.

work_wait_time = 241 # Time in minutes between running the work command. Default: 421

collect_wait_time = 16 # Time in minutes between running the collect colland. Default: 16

@tasks.loop(minutes=work_wait_time)
async def auto_work(work, channel, dep):
    await work.__call__(channel=channel) # Run the work command
    await deposit(dep, channel) # Deposit your newly earned money


@tasks.loop(minutes=collect_wait_time)
async def auto_collect(collect, channel, dep):
    await sleep(2) # Wait a few seconds for safety
    await collect.__call__(channel=channel) # Run the collect command
    await deposit(dep, channel) # Deposit your newly earned money


async def deposit(deposit, channel):
    await sleep(1) # Wait a second for safety
    await deposit.__call__(channel=channel, amount="all") # Run the deposit command


client = Client() # Define client session


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}') # Let the user know that its running


@client.event
async def on_message(message):
    if message.guild.id in guild_ids and message.author.id == client.user.id and message.content == "!start": # A few safety checks to make sure its not on accident
        await message.delete() # Delete command message
        guild = client.get_guild(message.guild.id) # Fetch current guild (Probably unnessesary)
        channel = guild.get_channel(message.channel.id) # Fetch current channel (Probably unnessesary)
        async for command in channel.slash_commands(command_ids=[901118136529588278, 901118136529588275, 901118136529588281]): # Fetches only necessary commands (deposit, collect, and work) for potential speedup
            if command.id == 901118136529588275: # Deposit command fetching
                deposit = command
            if command.id == 901118136529588278: # Collect command fetching
                collect = command
            if command.id == 901118136529588281: # Work command fetching
                work = command
        if auto_work.is_running() and auto_collect.is_running(): # Checks if they are already running
            auto_work.restart(work, channel, deposit) # Restarts work if already running
            auto_collect.restart(collect, channel, deposit) # Restarts collect if already running
        else:
            auto_work.start(work, channel, deposit) # Starts work if not running. REMOVE THIS ENTIRE LINE TO DISABLE THE WORK COMMAND
            auto_collect.start(collect, channel, deposit) # Starts collect if not running. REMOVE THIS ENTIRE LINE TO DISABLE THE COLLECT COMMAND
    if message.guild.id in guild_ids and message.author.id == client.user.id and message.content == "!stop": # A few safety checks to make sure its not on accident
        await message.delete() # Delete command message
        auto_work.stop() # Stop working
        auto_collect.stop() # Stop collecting

client.run("TOKEN")
