import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
	def _init_(self, client):
		self.client = client
	
	@commands.command()
	async def join(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("Join any Voice Channel")
		voice_channel = ctx.author.voice.channel
		if ctx.voice_client is None:
			await voice_channel.connect()
		else:
			ctx.voice_client.move_to(voice_channel)
			
	@commands.command()
	async def disconnect(self, ctx):
		await ctx.voice_client.disconnect()
      
def setup(client):
	client.add_cog(music(client)
