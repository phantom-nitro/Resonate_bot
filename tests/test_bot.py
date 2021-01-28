# dated : 27th jan

import discord
import random
from random import choice
from discord.ext import commands, tasks
from PIL import Image,ImageFilter
from io import BytesIO

#client: bot variable,bot accessed with this.
client = commands.Bot(command_prefix=';')
status = ['Music', 'Movie', 'Surangani Bad Words Remix', 'Adichi Thooku Bad Words Remix', 'Rocket League', 'Rainbow Six Siege','Valorant', 'Slapping Hydrogene', 'VJ mulla', 'Ankan PRO', 'Prime Leader Sudeep', 'Sao Sao_/\_', 'Get Burgified']

@client.event #allows to do certain action when certain event occurs
async def on_ready():
    change_status.start()
    general_channel = client.get_channel(759482792265908238)
    #await general_channel.send('up nd runnin..!')
    #wait for channel to be retrived and then message can be sent(as it is running async.)

@tasks.loop(seconds = 20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

@client.command()
async def rip(ctx,member:discord.Member=None):
    if not member:
        member =  ctx.author

    rip = Image.open('rip.png')
    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((257,187))
    rip.paste(pfp,(67,258))
    rip.save('prip.png')
    await ctx.send(file = discord.File('prip.png'))
