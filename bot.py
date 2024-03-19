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
    # with open("data\male_idols.csv", 'r', encoding="utf-8") as f:
    with open("data\male_idols_with_pics.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        chosen_row = random.choice(list(reader))
        stage_name =  chosen_row[0]
        korean_name = chosen_row[2]
        group = chosen_row[3]
        idol_picture_url = chosen_row[5]
    
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    # print(f"Fetching picture for {stage_name} from {group}")
    # idol_picture_url = scrape_idol_image(stage_name, group)
    # print(f"url: {idol_picture_url}")
    embed.set_image(url=idol_picture_url) 

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
    idol_picture_url = scrape_idol_image(stage_name, group)
    print(f"url: {idol_picture_url}")
    embed.set_image(url=idol_picture_url) 
    # embed.set_image(url='https://static.wikia.nocookie.net/kep1er/images/3/38/Youngeun_Magic_Hour_%28Sunkissed_Ver%29_Concept_Photo_1.jpeg/revision/latest?cb=20230916010214')

    await ctx.send(embed=embed)


bot.run(TOKEN)