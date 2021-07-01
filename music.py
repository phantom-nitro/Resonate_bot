import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def _init_(self, client):
        self.client = client
      
def setup(client):
    client.add_cog(music(client)
