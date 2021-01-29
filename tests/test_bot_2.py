from asyncio.windows_events import NULL
import discord
import random
from random import choice
from discord.ext import commands, tasks
from PIL import Image,ImageFilter
from io import BytesIO
import json
import os
import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://goucric:gnq316@cluster0.ymixq.mongodb.net/discordBot?retryWrites=true&w=majority")
db = client['discordBot']
col = db['mainbank']


os.chdir("D:\\discord_bot")

client = commands.Bot(command_prefix=';')
status = ['Music', 'Movie', 'Surangani Bad Words Remix', 'Adichi Thooku Bad Words Remix', 'Rocket League', 'Rainbow Six Siege','Valorant', 'Slapping Hydrogene', 'VJ mulla', 'Ankan PRO', 'Prime Leader Sudeep', 'Sao Sao_/\_', 'Get Burgified']

@client.event #allows to do certain action when certain event occurs
async def on_ready():
    change_status.start()
    general_channel = client.get_channel(759482792265908238)

@tasks.loop(seconds = 20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users=col.find_one({'user_id':str(user.id)})
    wallet_amt = users["wallet"]
    bank_amt =  users["bank"]
    em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
    em.add_field(name = "wallet",value=wallet_amt)
    em.add_field(name = "bank balance",value=bank_amt)
    await ctx.send(embed = em)

@client.command()
async def beg(ctx):
        await open_account(ctx.author)
        user = ctx.author
        users=col.find_one({'user_id':str(user.id)})
        earnings = random.randrange(101)
        await ctx.send(f"eli gave you {earnings} coins!!")
        total = users["wallet"] + earnings
        col.update_one({'user_id':str(user.id)}, {"$set": { "wallet":  total}})

async def open_account(user):
        
    users=col.find_one({'user_id':str(user.id)})
    if users:
        return False
    else:
        users = {'user_id':str(user.id),"wallet":0,"bank":0}  
    col.insert_one(users)
    return True



client.run('ODA0MDEzNjQzNjQ4OTkxMjUy.YBGKDg.k3e0j0FmWktzP8shgmhI-fStekk')
