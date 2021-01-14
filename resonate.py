import discord
import os
import random
import quote_eg_joke
import time
import json
from typing import Optional
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from random import choice
#from chatbot import Chat, register_call

#os.chdir("C:\\Users\\Admin\\Document\\python")

events = [1, 0]
token = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = ';')
client.remove_command('help')
status = ['Music', 'Movie', 'Surangani Bad Words Remix', 'Adichi Thooku Bad Words Remix', 'Rocket League', 'Rainbow Six Siege','Valorant', 'Slapping Hydrogene', 'VJ mulla', 'Ankan PRO', 'Prime Leader Sudeep', 'Sao Sao_/\_', 'Get Burgified']
players = {}

#template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbotTemplate", "chatbottemplate.template")
#chat = Chat(template_file_path)


@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready.')
@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
    #raise error  # re-raise the error so all the errors will still show up in console


@tasks.loop(seconds = 20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

@client.command(aliases = ["bal"])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
    em.add_field(name = 'Wallet balance', value = wallet_amt, inline = False)
    em.add_field(name = 'Bank balance', value = bank_amt, inline = False)
    await ctx.send(embed = em)

@client.command(aliases = ["res"])
async def respect(ctx):
    await open_account_respect(ctx.author)
    user = ctx.author
    users = await get_respect_data()

    respect_amt = users[str(user.id)]["respect"]
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



@client.command(aliases = ["lb"])
async def leaderboard(ctx, x = 5):

    users = await get_respect_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["respect"]
        leader_board[total_amount] = name
        total.append(total_amount)
    total = sorted(total, reverse = True)
    em = discord.Embed(title = f"Top {x} Respect Points holders", description = "Leaderboard", color = discord.Color.red())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        em.add_field(name = f"{index}. {member}", value = f"{amt}", inline = False)
        if index == x:
            break
        else:
            index += 1
    await ctx.send(embed = em)


@client.command(aliases = ["req", "request"])
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(1001)
    await ctx.send(f"Resonate gave **{ctx.author}** {earnings} coins!")

    users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)

@client.command(aliases = ["with"])
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send(f"**{ctx.author}** Please enter the Amount")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send(f"**{ctx.author}** You don't have that much Money")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author}** Amount must be Positive")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    await ctx.send(f"**{ctx.author}** withdrew {amount} coins")

@client.command(aliases = ["dep"])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send(f"**{ctx.author}** Please enter the Amount")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send(f"**{ctx.author}** You don't have that much Money")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author}** Amount must be Positive")
        return

    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount, "bank")
    await ctx.send(f"**{ctx.author}** deposited {amount} coins")

@client.command(aliases = ["gift"])
async def send(ctx, member:discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send(f"**{ctx.author}** Please enter the Amount")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send(f"**{ctx.author}** You don't have that much Money")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author}** Amount must be Positive")
        return

    await update_bank(ctx.author, -1*amount, "bank")
    await update_bank(member, amount, "bank")
    await ctx.send(f"**{ctx.author}** gave {amount} coins to {member}")

@client.command()
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send(f"**{ctx.author}** Please enter the Amount")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send(f"**{ctx.author}** You don't have that much Money")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author}** Amount must be Positive")
        return

    final = []
    for i in range(3):
        a = random.choice(["<:meme_stare:787584294977667104>", "<:meme_cj_happy:780812567252828170>", "<:meme_shrek:780808598523215902>"])
        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] and final[0] == final[2] and final[2] == final[1]:
        await update_bank(ctx.author, 2*amount)
        await ctx.send(f"{ctx.author} You Won double the amount you bet!")
    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send(f"{ctx.author} You Lost")



async def open_account(user):

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True
async def open_account_respect(user):

    users = await get_respect_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["respect"] = 0

    with open("respect.json", "w") as f:
        json.dump(users, f)
    return True
async def get_respect_data():
    with open("respect.json", "r") as f:
        users = json.load(f)
    return users

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change = 0, mode = 'wallet'):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]['wallet'], users[str(user.id)]['bank']]
    return bal

#@client.command(pass_context = True)
#async def ai(ctx, *, message):
#    result = chat.respond(message)

#    embed = discord.Embed(title = "Resonate AI", description = result, color = (0xF7FF00))
#    await ctx.send(embed = embed)


@client.command(name='ping', help = 'return Latency')
async def ping(ctx):
	await ctx.send(f':zap: Latency: {round(client.latency*1000)}ms')


@client.command(pass_context = True)
async def help(ctx, cmd: Optional[str]):
    if cmd is None:

        embed = discord.Embed(color = discord.Colour.teal())
        embed.set_author(name = 'Help')
        embed.add_field(name = 'How it works?', value = 'Whoever gets Respect points 6000(THE IMPOSSIBLE) is the Master of the Universe [for now]', inline = False)
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
    results = random.choices(events, weights = [95, 5])
    if results == [1]:
        await ctx.send('no u')
    else:
        await ctx.send(f"Ahh! I'm tired. {ctx.author.name} won")
        await ctx.send('Respect + 5')
        await open_account_respect(ctx.author)
        users = await get_respect_data()
        user = ctx.author

        respect_points = 5

        users[str(user.id)]["respect"] += respect_points
        with open("respect.json", "w") as f:
            json.dump(users, f)


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
        results = random.choices(events, weights = [58, 42])
        if results == [1]:
            await ctx.send(f'{ctx.author.name} Respect + 4')
            await open_account_respect(ctx.author)
            users = await get_respect_data()
            user = ctx.author

            respect_points = 4

            users[str(user.id)]["respect"] += respect_points
            with open("respect.json", "w") as f:
                json.dump(users, f)
    elif te == 'add':
        quote_eg_joke.valnew.append(cmd)
        print(cmd)
        await ctx.send("Your New Quote has been Successfully added. It will be visible in the next run <:meme_cj_happy:780812567252828170>")


@client.command(aliases = ["easteregg"])
async def eg(ctx):
    results = random.choices(events, weights = [95, 5])
    if results == [1]:
        await ctx.send('`You need to try hard to get the code`')
    else:
        results = random.choices(quote_eg_joke.egg)
        await ctx.send(*results)
        await ctx.send(f'Congradulations! {ctx.author.name} has Unlocked Secret command. Respect + 10 <:anime_awoo:780805005808107530>')
        await open_account_respect(ctx.author)
        users = await get_respect_data()
        user = ctx.author

        respect_points = 10

        users[str(user.id)]["respect"] += respect_points
        with open("respect.json", "w") as f:
            json.dump(users, f)


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
    #elif message[0] == 'c':
        #msg, hexc = message.split(' ')
        #hexc = hexc[-6:]
        #print(int(hexc))
        #hex_int = int(hexc, 16)
        #new_int = hex_int + 0x200
        #embed = discord.Embed( description = '<- here is your color', color = hex(new_int))
        #await ctx.send(embed = embed)

    else:
        await ctx.send('This is not a Special code')





        


client.run(token)