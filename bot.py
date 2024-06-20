import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import csv
import random
from idol_scraper import scrape_idol_image
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
emojis = ["♥️", "💓", "💗", "🩷", "💜", "💘", "💖"]
base_url = "http://127.0.0.1:5000/"

@bot.command()
async def mi(ctx):
    url = base_url + "/idols/random-idol/male"
    response = requests.get(url)
    idol_info = response.json()
    stage_name = idol_info['stage_name']
    korean_name = idol_info['korean_name']
    group = idol_info['group']
    idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + idol_info['picture_url']
 
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    embed.set_image(url=idol_picture_url) 
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(random.choice(emojis))


@bot.command()
async def fi(ctx):
    url = base_url + "/idols/random-idol/female"
    response = requests.get(url)
    idol_info = response.json()
    stage_name = idol_info['stage_name']
    korean_name = idol_info['korean_name']
    group = idol_info['group']
    idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + idol_info['picture_url']

    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
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