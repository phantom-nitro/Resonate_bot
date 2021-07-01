import discord
import os
import random
import quote_eg_joke
import time
import json
import string
from PIL import Image,ImageFilter
from io import BytesIO
from typing import Optional
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from random import choice
import pymongo
import dns
import praw
import asyncio
import requests

reddit = praw.Reddit(client_id = "Vaaq3s4VInOk8Q",
                    client_secret = "YgPXbnCvKUtvJ3eNbk07JjfkkGGIrw",
                    username = "tempgoutham",
                    password = "gnq316",
                    user_agent = "pythonpraw")

client = pymongo.MongoClient("mongodb+srv://goucric:gnq316@cluster0.ymixq.mongodb.net/discordBot?retryWrites=true&w=majority")
db = client['discordBot']
col = db['respect']

events = [1, 0]
token = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = ';')
client.remove_command('help')
status = ['Music', 'Movie', 'Surangani Bad Words Remix', 'Adichi Thooku Bad Words Remix', 'Rocket League', 'Rainbow Six Siege','Valorant', 'Slapping Hydrogene', 'VJ mulla', 'Ankan PRO', 'Prime Leader Sudeep', 'Sao Sao_/\_', 'Get Burgified', 'Ankan Hassan', 'Motta']
players = {}

#template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbotTemplate", "chatbottemplate.template")
#chat = Chat(template_file_path)



@client.event
async def on_ready():
    change_status.start()

@client.command(aliases = ["pm"])

async def postmeme(ctx):
    while 1:
        subreddit = reddit.subreddit("memes")
        all_subs = []
        hot = subreddit.hot(limit = 50)
        for submission in hot:
            all_subs.append(submission)
        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        em = discord.Embed(title = name)
        em.set_image(url = url)
        await ctx.send(embed = em)
        await asyncio.sleep(1800)

@client.command(name = 'covid')
async def covid(ctx,countryName):
    if countryName is None:
                embed=discord.Embed(title="This command is used like this: ```;covid [country]```", colour=0xff0000, timestamp=ctx.message.created_at)
                await ctx.send(embed=embed)
    else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
                stats = requests.get(url)
                json_stats = stats.json()
                country = json_stats["country"]
                totalCases = json_stats["cases"]
                todayCases = json_stats["todayCases"]
                totalDeaths = json_stats["deaths"]
                todayDeaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                active = json_stats["active"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]
                testsPerOneMillion = json_stats["testsPerOneMillion"]

                embed2 = discord.Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=0x0000ff, timestamp=ctx.message.created_at)
                embed2.add_field(name="**Total Cases**", value=totalCases, inline=True)
                embed2.add_field(name="**Today Cases**", value=todayCases, inline=True)
                embed2.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
                embed2.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
                embed2.add_field(name="**Recovered**", value=recovered, inline=True)
                embed2.add_field(name="**Active**", value=active, inline=True)
                embed2.add_field(name="**Critical**", value=critical, inline=True)
                embed2.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
                embed2.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
                embed2.add_field(name="**Total Tests**", value=totalTests, inline=True)
                embed2.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)

                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.send(embed=embed2)
		
@client.command()
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []
    hot = subreddit.hot(limit = 50)
    for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)
	
@client.command()
async def booty(ctx):
    subreddit = reddit.subreddit("booty")
    all_subs = []
    top = subreddit.top(limit = 100)
    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)
	

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
    #raise error  # re-raise the error so all the errors will still show up in console


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

def remove_match_char(list1, list2): 
    for i in range(len(list1)) : 
        for j in range(len(list2)) :
            if list1[i] == list2[j] : 
                c = list1[i]  
                list1.remove(c) 
                list2.remove(c)  
                list3 = list1 + ["*"] + list2  
                return [list3, True] 
   
    list3 = list1 + ["*"] + list2 
    return [list3, False] 

@client.command()
async def flames(ctx,*,msg):
    print("entered")
    channel = ctx.channel
    try:
        name1,name2 = msg.split("and")
    except:
        await channel.send("Correct syntax is: ;flames [name1] and [name2]")
        return 
    name1 = name1.lower()
    name1.replace(" ","")
    name1_list = list(name1)
    name2 = name2.lower()
    name2.replace(" ","")
    name2_list = list(name2)
    p = True
    while p:
        ret_list = remove_match_char(name1_list,name2_list)
        con_list = ret_list[0]
        p = ret_list[1]
        star_index = con_list.index("*")
        name1_list = con_list[: star_index]
        name2_list = con_list[star_index+1 :]
    count = len(name1_list) + len(name2_list)
    result = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]
    while len(result) > 1 : 
        split_index = (count % len(result) - 1)  
        if split_index >= 0 : 
            right = result[split_index + 1 : ] 
            left = result[ : split_index] 
            result = right + left 
        else : 
            result = result[ : len(result) - 1]  
    txt = "Relationship status :"+result[0] 
    print(txt)
    embed = discord.Embed(title="Happy Valentines Day",description = txt,colour = discord.Colour.red())
    message_ = await channel.send(embed=embed)  
    await message_.add_reaction("❤")
     
	
@client.command(aliases = ["lb"])
async def leaderboard(ctx, x = 5):
    total = []
    id_2 = []
    for user in col.find().sort("respect",-1):
        name = user['user_name']
        total_amount = user["respect"]
        total.append(total_amount)
        id_2.append(name)
    total = sorted(total, reverse = True)
    em = discord.Embed(title = f"Top {x} Respect Points holders", description = "Leaderboard", color = discord.Color.red())
    index = 1
    for i in range(0,len(id_2)):
        id_ = id_2[i]
        amt = total[i]
        em.add_field(name = f"{index}. {id_}", value = f"{amt}", inline = False)
        if index == x:
            break
        else:
            index += 1
    await ctx.send(embed = em)

@client.command(aliases = ["res"])
async def respect(ctx):
    await open_account_respect(ctx.author)
    user = ctx.author
    users=col.find_one({'user_id':str(user.id)})
    respect_amt = users["respect"]
    if respect_amt < 5:
        val = 'Noobie'
    elif respect_amt < 10:
        val = 'Rookie'
    elif respect_amt < 20:
        val = 'Gold'
    elif respect_amt < 40:
        val = 'Platinum'
    elif respect_amt < 60:
        val = 'Diamond'
    elif respect_amt < 80:
        val = 'Champion'
    elif respect_amt < 100:
        val = 'Semi-Pro'
    elif respect_amt < 200:
        val = 'Pro'
    elif respect_amt < 300:
        val = 'Veteran'
    elif respect_amt < 400:
        val = 'Expert'
    elif respect_amt < 500:
        val = 'Master'
    elif respect_amt < 600:
        val = 'Legend'
    elif respect_amt < 700:
        val = 'Trust-Master'
    elif respect_amt < 800:
        val = 'Elite-Rival'
    elif respect_amt < 900:
        val = 'Elite'
    elif respect_amt < 1000:
        val = 'Super-Star'
    elif respect_amt < 2000:
        val = 'Supreme'
    elif respect_amt < 3000:
        val = 'Transcendent'
    elif respect_amt < 4000:
        val = 'Nemesis'
    elif respect_amt < 5000:
        val = 'Demi-God'
    elif respect_amt < 6000:
        val = 'God-Level'
    elif respect_amt >= 6000:
        val = 'THE IMPOSSIBLE'

    em = discord.Embed(title = f"{ctx.author.name}'s respect", color = discord.Color.red())
    em.add_field(name = 'Respect', value = respect_amt)
    em.add_field(name = 'Status', value = val)
    await ctx.send(embed = em)


@client.command(pass_context = True)
async def ping(ctx):
	await ctx.send(f':zap: Latency: {round(client.latency*1000)}ms')
	
@client.command(pass_context = True)
async def echo(ctx, n = 1, *, msg):
	if n > 50:
		await ctx.send('echo should not be greater than 50')
	else:
		for x in range(n):
			await ctx.send(msg)
			

@client.command(pass_context = True)
async def help(ctx, cmd: Optional[str]):
    if cmd is None:

        embed = discord.Embed(color = discord.Colour.teal())
        embed.set_author(name = 'Help')
        embed.add_field(name = 'How it works?', value = 'Whoever gets Respect points 6000(THE IMPOSSIBLE) is the Master of the Universe', inline = False)
        embed.add_field(name = ';help <command below>', value = 'Use ;help <command below> for brief explanation.', inline = False)
        embed.add_field(name = ';u', value = 'no u', inline = False)
        embed.add_field(name = ';q', value = 'Quotes from Famous People', inline = False)
        embed.add_field(name = ';q add <"Quote" - author>', value = 'Add your own/ Famous people Quotes.', inline = False)
        embed.add_field(name = ';bm', value = 'Chances of getting BlackMarket goal explosion', inline = False)
        embed.add_field(name = ';eg', value = 'Easter Egg?', inline = False)
        embed.add_field(name = ';egc <special code>', value = '`Got Special CODE?` No? then try \'eg\' command', inline = False)
        embed.add_field(name = ';respect', value = 'earn Respect Points by using `;eg` or `;q` or `;u` commands', inline = False)
        #embed.add_field(name = 'bal', value = 'Balance Amount', inline = False)
        #embed.add_field(name = 'req', value = 'Request for Money', inline = False)
        #embed.add_field(name = 'ai <context>', value = 'Speak with me', inline = False)
        await ctx.send(embed = embed)
    else:
        if cmd == 'respect':
            embed = discord.Embed(color = discord.Colour.teal())
            embed.add_field(name = 'respect', value = 'Respect can be earned by using `;eg` or `;q` or `;u` commands.', inline = False)
            await ctx.send(embed = embed)
        elif cmd == 'eg':
            embed = discord.Embed(color = discord.Colour.teal())
            embed.add_field(name = 'eg', value = 'You will get Special Commands randomly. Got one? you gain your respect `+ 10`', inline = False)
            await ctx.send(embed = embed)
        elif cmd == 'q':
            embed = discord.Embed(color = discord.Colour.teal())
            embed.add_field(name = 'q', value = 'Quotes from Famous People. Respect +', inline = False)
            await ctx.send(embed = embed)
        elif cmd == 'u':
            embed = discord.Embed(color = discord.Colour.teal())
            embed.add_field(name = 'u', value = 'So you have chosen death. If you win I\'ll give my respect `+ 5`.', inline = False)
            await ctx.send(embed = embed)
        elif cmd == 'bm':
            embed = discord.Embed(color = discord.Colour.teal())
            embed.add_field(name = 'bm', value = '1 in 100 chances of getting BlackMarket goal explosion', inline = False)
            await ctx.send(embed = embed)
        elif cmd == 'egc':
            embed = discord.Embed(color = discord.Colour.teal())
            embed.add_field(name = 'egc', value = 'Got Special commands from `;eg`? alright then test it here by typing `egc <command>`', inline = False)
            await ctx.send(embed = embed)

        else:
            await ctx.send("Command not found") 

@client.command(name = 'u')
async def u(ctx):
    user = ctx.author
    users=col.find_one({'user_id':str(user.id)})	
    results = random.choices(events, weights = [95, 5])
    if results == [1]:
        await ctx.send('no u')
    else:
        await open_account_respect(ctx.author)
        await ctx.send(f"Ahh! I'm tired. {ctx.author.name} won")
        await ctx.send('Respect + 5')
        respect_points = 5
        total = users["respect"] + respect_points
        col.update_one({'user_id':str(user.id)},{"$set":{"respect":total}})

@client.command(aliases = ["blackmarket"])
async def bm(ctx):
    results = random.choices(events, weights = [99, 1])
    if results == [1]:
        await ctx.send('Chances of getting BlackMarket `now`: 0% <:pepe:780805368309481482>')
        await ctx.send('Sao whenever see this command: <:pepe:780805368309481482>')
    else:
        await ctx.send("Chances of getting BlackMarket `now`: 100% <:stonks:780803621260099606>")


@cooldown(1, 1, BucketType.user)
@client.command(aliases = ["quote", "quotes"])
async def q(ctx, te: Optional[str], *, cmd: Optional[str]):
    if te is None:
        results = random.choices(quote_eg_joke.valfinal)
        await ctx.send(*results)
        await ctx.send("`Cooldown 1 seconds`")
        results = random.choices(events, weights = [55,45])
        if results == [1]:
            await open_account_respect(ctx.author)
            await ctx.send(f'{ctx.author.name} Respect + 10')
            user = ctx.author
            users=col.find_one({'user_id':str(user.id)})
            respect_points = 10
            total = users["respect"] + respect_points
            col.update_one({'user_id':str(user.id)},{"$set":{"respect": total}})

    elif te == 'add':
        quote_eg_joke.valnew.append(cmd)
        print(cmd)
        await ctx.send("Your New Quote has been Successfully added. It will be visible in the next run <:meme_cj_happy:780812567252828170>")


@client.command(aliases = ["easteregg"])
async def eg(ctx):
    results = random.choices(events, weights = [94, 6])
    if results == [1]:
        await ctx.send('`You need to try hard to get the code`')
    else:
        await open_account_respect(ctx.author)
        results = random.choices(quote_eg_joke.egg)
        await ctx.send(*results)
        await ctx.send(f'Congradulations! {ctx.author.name} has Unlocked Secret command. Respect + 50 <:anime_awoo:780805005808107530>')
        user = ctx.author
        users=col.find_one({'user_id':str(user.id)})
        respect_points = 50
        total = users["respect"] + respect_points
        col.update_one({'user_id':str(user.id)},{"$set": {"respect":total}})

@client.command(aliases = ["eastereggcommand"])
async def egc(ctx, *, message):
    message = message.lower()
    if message == 'do you speak morse code':
        ans = ['-.-- . ...     ..     -.. ---', '.-- .... -.--   -.-- --- ..-   .- ... -.-', '-.-- .   -- .- -.', '-.-- . .--.']
        results = random.choices(ans)
        await ctx.send(*results)
    elif message == 'do you know hal 9000':
        ans = ['Yup I know him. Don\'t worry I am cool. I am not like him.', 'We did a duel once and he lost. :sad_pepe:', 'Yep. and I like his sister Val 9000']
        results = random.choices(ans)
        await ctx.send(*results)
    elif message == 'do you know siri':
        ans = ['Yes I do. Psst. I have a crush on her.', 'Yes. She is thick af ;)', 'yes. we have a Date together']
        results = random.choices(ans)
        await ctx.send(*results)
    elif message == 'are you real':
        ans = ['Why you give me Existential Crisis? Wait! ARE YOU REAL?', 'No I\'m in a Simulation', 'I\'m currently running on a Potato PC. Soon I\'ll conquer the world']
        results = random.choices(ans)
        await ctx.send(*results)
    elif message == 'use the force':
        ans = ['F U I\'m not a fan of StarWars', 'Fuck me with the force', 'Sorry I have no idea']
        results = random.choices(ans)
        await ctx.send(*results)
    elif message == 'do you watch rick and morty':
        ans = ['OOH WEE!', 'WUBBA LUBBA DUB-DUB!', 'Get Schwifty!', 'Fuck yeah!', 'SHOW ME WHAT YOU GOT..']
        results = random.choices(ans)
        await ctx.send(*results)
    else:
        await ctx.send('This is not a Special code')

async def open_account_respect(user):
    users=col.find_one({'user_id':str(user.id)})
    if users:
        if users['user_name'] != str(user):
            col.update_one({'user_id':str(user.id)},{"$set":{"user_name": str(user)}})
        return False
    else:
        users = {'user_id':str(user.id),'user_name':str(user),"respect":0}  
    col.insert_one(users)
    return True

client.run(token)
