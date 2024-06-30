import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
emojis = ["♥️", "💓", "💗", "🩷", "💜", "💘", "💖"]
base_url = "http://127.0.0.1:5000"

@bot.command()
async def mi(ctx):
    # get random idol 
    idol_request_url = base_url + "/idols/random-idol/male"
    response = requests.get(idol_request_url)
    idol_info = response.json()
    print(f"IDOL ID: {idol_info['id']}")
    stage_name, korean_name, group = idol_info['stage_name'], idol_info['korean_name'], idol_info['group']
    idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + idol_info['picture_url']
 
    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    embed.set_image(url=idol_picture_url) 

    # check if idol has been claimed by anyone in the server
    status_request_url = base_url + f"/idols/?idolID={idol_info['id']}&serverID={ctx.guild.id}"
    response = requests.get(status_request_url)
    status_info = response.json()

    if (status_info['claimed']):                # if claimed, output idol but unclaimable
        embed.set_footer(text=f"Claimed by {status_info['username']}")
        print(f"Claimed by {status_info['username']}")
        msg = await ctx.send(embed=embed)
    else:                                       # if unclaimed, idol is claimable via reaction
        msg = await ctx.send(embed=embed)
        emoji = random.choice(emojis)
        await msg.add_reaction(emoji)

        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) == emoji and reaction.message.id == msg.id
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)

            claimed = add_claimed(user.id, user.name, ctx.guild.id, idol_info['id'])        # update idol to be claimed (create User, User_Server, Idol_Server)
            if (claimed):
                await ctx.send(f"{emoji} **{user.name}** claimed **{stage_name}** as their bias! {emoji}")
                print(f"User name: {user.name} | User ID: {user.id} | Server name: {ctx.guild.name} | Server ID: {ctx.guild.id}")
            else:
                await ctx.send(f"Error claiming {stage_name} for {user.name}")
        except asyncio.TimeoutError:
            await ctx.send(f"Ran out of time to claim {stage_name}")

@bot.command()
async def fi(ctx):
    # get random idol 
    idol_request_url = base_url + "/idols/random-idol/female"
    response = requests.get(idol_request_url)
    idol_info = response.json()
    stage_name, korean_name, group = idol_info['stage_name'], idol_info['korean_name'], idol_info['group']
    idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + idol_info['picture_url']

    embed = discord.Embed(
        color=discord.Color.pink(),
        description=group,
        title=f"{stage_name} ({korean_name})"
    )
    embed.set_image(url=idol_picture_url) 

    # check if idol has been claimed by anyone in the server
    status_request_url = base_url + f"/idols/?idolID={idol_info['id']}&serverID={ctx.guild.id}"
    response = requests.get(status_request_url)
    status_info = response.json()

    if (status_info['claimed']):                # if claimed, output idol but unclaimable
        embed.set_footer(text=f"Claimed by {status_info['username']}")
        print(f"Claimed by {status_info['username']}")
        msg = await ctx.send(embed=embed)
    else:                                       # if unclaimed, idol is claimable via reaction
        msg = await ctx.send(embed=embed)
        emoji = random.choice(emojis)
        await msg.add_reaction(emoji)

        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) == emoji and reaction.message.id == msg.id
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)

            claimed = add_claimed(user.id, user.name, ctx.guild.id, idol_info['id'])        # update idol to be claimed (create User, User_Server, Idol_Server)
            if (claimed):
                await ctx.send(f"{emoji} **{user.name}** claimed **{stage_name}** as their bias! {emoji}")
                print(f"User name: {user.name} | User ID: {user.id} | Server name: {ctx.guild.name} | Server ID: {ctx.guild.id}")
            else:
                await ctx.send(f"Error claiming {stage_name} for {user.name}")
        except asyncio.TimeoutError:
            await ctx.send(f"Ran out of time to claim {stage_name}")

@bot.command()
async def info(ctx, first_word, *args):
    if (len(args) > 0):
        arguments = ' '.join(args)
        query = first_word + ' ' + arguments
    else:
        query = first_word

    request_url = base_url + f"/idols/info?query={query}"
    response = requests.get(request_url).json()
    if (response["found"]):
        results = response["results"]
        if len(results) > 1:
            description = f"\n**Number of results:** {len(results)}\n\n"
            for idol in results:
                group = idol['group'] if idol['group'] else None
                if (group != None):
                    description += f"**{idol['stage_name']}** - {group}\n"
                else:
                    description += f"**{idol['stage_name']}**\n"
            embed = discord.Embed(
                color=discord.Color.pink(),
                description=description)
        else:
            idol_info = results[0]
            description = f"Full Name: {idol_info['full_name']}\n Korean Name: {idol_info['korean_name']}\n Group: {idol_info['group']}\n Country: {idol_info['country']}\n"
            embed = discord.Embed(
                color=discord.Color.pink(),
                description=description)

            idol_id = idol_info['id']
            request_url = base_url + f"/idols/{idol_id}"
            response = requests.get(request_url)
            idol_picture_url = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + response.json()['picture_url']  
            embed.set_image(url=idol_picture_url) 

            embed.set_author(name=f"{idol_info['stage_name']}")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Idol not found :(")

@bot.command()
async def collection(ctx):
    request_url = base_url + f"/users/collection?userID={ctx.message.author.id}&serverID={ctx.guild.id}"
    response = requests.get(request_url).json()
    description = f"\n**Number of idols:** {len(response)}\n\n"
    counter = 1
    if len(response) > 0:
        for idol in response:
            group = idol['group'] if idol['group'] else None
            description += f"**#{counter}** - {idol['stage_name']}  |  Group: {group}\n"
            counter += 1

        embed = discord.Embed(
            color=discord.Color.pink(),
            description=description
        )
        first_idol_id = response[0]['id']
        request_url = base_url + f"/idols/{first_idol_id}"
        response = requests.get(request_url)
        first_idol_picture = "https://bias-bot-images.s3.us-west-1.amazonaws.com/" + response.json()['picture_url']

        embed.set_thumbnail(url=first_idol_picture)
        embed.set_author(name=f"{ctx.message.author.name}'s collection", icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            color=discord.Color.pink(),
            description="Empty :("
        )
        embed.set_thumbnail(url=ctx.message.author.avatar.url)
        embed.set_author(name=f"{ctx.message.author.name}'s collection", icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed)


# commands to add or remove servers from database
@bot.event
async def on_guild_join(guild):
    print(f'Joined guild: {guild.name} | ID: {guild.id}')
    url = base_url + "/servers"
    body = {"server_id": guild.id, "name": guild.name}

    response = requests.post(url, json=body)
    print(f"penis: {response}")

@bot.event
async def on_guild_remove(guild):
    print(f'Left guild: {guild.name} | ID: {guild.id}')
    url = base_url + "/servers/" + str(guild.id)
    requests.delete(url)


# util commands
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


def add_claimed(user_id, username, server_id, idol_id):
    add_user_url = base_url + "/users"
    body = {"user_id": user_id, "username": username}
    user_info = requests.post(add_user_url, json=body)      # add user to database
    response = user_info.json()

    if (response["created"]):  # if user already exists in database or successfully created
        add_claimed_url = base_url + "/users/claimed"
        body = {"user_id": response['user_id'], "username": username, "idol_id": idol_id, "server_id": server_id}
        claimed_info = requests.post(add_claimed_url, json=body)
    
    if claimed_info.status_code == 200:
        return True
    else:
        return False

bot.run(TOKEN)