import logging
import os
import discord
from discord.ext import commands
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix="$")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")    


client.run("NjQ0NzQ4OTYzNDU0NjQ4MzIw.Xc4nWw.mGPHYFltXUEXkwLNg7VzdJkG-WA")
