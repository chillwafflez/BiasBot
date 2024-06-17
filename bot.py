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
emojis = ["♥️", "💓", "💗", "🩷", "💜", "💘", "💖"]

@bot.command()
async def mi(ctx):
    stage_name = ""
    korean_name = ""
    group = ""
    with open("data\male_idol_filenames.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        chosen_row = random.choice(list(reader))
        stage_name =  chosen_row[0]
        korean_name = chosen_row[2]
        group = chosen_row[3]
        idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + chosen_row[5]
    
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    # print(f"Fetching picture for {stage_name} from {group}")
    # idol_picture_url = scrape_idol_image(stage_name, group)
    # print(f"url: {idol_picture_url}")
    embed.set_image(url=idol_picture_url) 
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(random.choice(emojis))


@bot.command()
async def fi(ctx):
    stage_name = ""
    korean_name = ""
    group = ""
    with open("data\\female_idol_filenames.csv", 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        chosen_row = random.choice(list(reader))
        stage_name =  chosen_row[0]
        korean_name = chosen_row[2]
        group = chosen_row[3]
        idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + chosen_row[5]
    
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    # print(f"Fetching picture for {stage_name} from {group}")
    # idol_picture_url = scrape_idol_image(stage_name, group)
    # print(f"url: {idol_picture_url}")
    embed.set_image(url=idol_picture_url) 
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(random.choice(emojis))

@bot.command()
async def guildInfo(ctx):
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    await ctx.send(f"Server name: {server_name} | Server ID: {server_id}")

@bot.command()
async def userID(ctx):
    user_name = ctx.message.author.name
    user_id = ctx.message.author.id
    user_nickname = ctx.message.author.nick
    await ctx.send(f"User name: {user_name} | User ID: {user_id} | Server nickname: {user_nickname}")


bot.run(TOKEN)