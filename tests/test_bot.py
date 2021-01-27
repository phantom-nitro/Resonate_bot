# dated : 27th jan

import discord

#client: bot variable,bot accessed with this.
client = discord.Client()

@client.event #allows to do certain action when certain event occurs
async def on_ready():
    general_channel = client.get_channel(759482792265908238)
    await general_channel.send('salam_Alaikum!')
    #wait for channel to be retrived and then message can be sent(as it is running async.)

client.run('ODA0MDEzNjQzNjQ4OTkxMjUy.YBGKDg.k3e0j0FmWktzP8shgmhI-fStekk')




#----------------------------
#804013643648991252 - bot id
#308b39f48942607ff24c08de04164ae2d44d05e399aa3dc7a1dcb846c629fa39 -public key
#ODA0MDEzNjQzNjQ4OTkxMjUy.YBGKDg.k3e0j0FmWktzP8shgmhI-fStekk -token