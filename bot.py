import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import csv
import random


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def mi(ctx):
    stage_name = ""
    korean_name = ""
    group = ""
    with open("data\male_idols.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        chosen_row = random.choice(list(reader))
        # msg = chosen_row[0] + " | " + chosen_row[2]
        stage_name =  chosen_row[0]
        korean_name = chosen_row[2]
        group = chosen_row[3]
    
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    # embed.set_author(f"{stage_name} ({korean_name})")
    embed.set_image(url="https://i.pinimg.com/736x/24/25/db/2425db29777df3fa81aa1544166fe448.jpg")

    await ctx.send(embed=embed)
    # await msg.add_reaction(":pink_heart:")

@bot.command()
async def fi(ctx):
    with open("data\\female_idols.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        chosen_row = random.choice(list(reader))
        msg = chosen_row[0] + " | " + chosen_row[2]

    await ctx.send(msg)


# @bot.command()
# async def help(ctx):
#     msg = "Type $mi to roll for male idols\nType $fi to roll female idols\nType $bi to roll for both"

#     await ctx.send(msg)

# client = discord.Client(intents=discord.Intents.default())

# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')

# @client.event
# async def on_message(message):
#     if message.content.startswith('////'):
#         await message.channel.send("COCK")

# client.run(TOKEN)
bot.run(TOKEN)