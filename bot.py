import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import csv
import random
from idol_scraper import scrape_idol_image


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
        stage_name =  chosen_row[0]
        korean_name = chosen_row[2]
        group = chosen_row[3]
    
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    print(f"Fetching picture for {stage_name} from {group}")
    idol_picture = scrape_idol_image(stage_name, group)
    embed.set_image(url=idol_picture)
    # embed.set_image(url="https://www.allkpop.com/upload/2023/04/content/191153/web_data/allkpop_1681919771_untitled-1.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def fi(ctx):
    stage_name = ""
    korean_name = ""
    group = ""
    with open("data\\female_idols.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        chosen_row = random.choice(list(reader))
        stage_name =  chosen_row[0]
        korean_name = chosen_row[2]
        group = chosen_row[3]
    
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    print(f"Fetching picture for {stage_name} from {group}")
    idol_picture = scrape_idol_image(stage_name, group)
    embed.set_image(url=idol_picture) 

    await ctx.send(embed=embed)


# @bot.command()
# async def help(ctx):
#     msg = "Type $mi to roll for male idols\nType $fi to roll female idols\nType $bi to roll for both"
#     embed = discord.Embed(
#         color=discord.Color.pink(),
#         description=msg,
#         title="Help"
#     )
#     await ctx.send(embed=embed)

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