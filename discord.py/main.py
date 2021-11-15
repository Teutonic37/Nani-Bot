import discord
import requests
import json
import os
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.utils import get
import random

client = commands.Bot(command_prefix="!")
client.remove_command("help")

os.chdir('C:\\Users\\vihaan\\PycharmProjects\\discord.py')

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def get_meme():
    content = requests.get("https://meme-api.herokuapp.com/gimme")
    data = json.loads(content.text)
    meme = discord.Embed(title=f"{data['title']}", Color=discord.Color.random()).set_image(url=f"{data['url']}")
    return meme


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' - ' + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if not message.author.bot:
        await open_account_level(message.author)
        users = await get_level_data()

        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)
    if not message.author.bot:
        user = message.author
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('!meme'):
        meme = get_meme()
        await message.reply(embed=meme)
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.command()
async def help(ctx):
    em = discord.Embed(title="Help command", color=discord.Color.red())
    info = "Get random motivational lines"
    em.add_field(name="!inspire", value=info, inline=True)
    info2 = "Get a random meme"
    em.add_field(name="!meme", value=info2, inline=True)
    info3 = "Check your economy details"
    em.add_field(name="!balance", value=info3, inline=True)
    info4 = "Check your level details"
    em.add_field(name="!level", value=info4, inline=True)
    info5 = "Play rock paper scissors"
    em.add_field(name="!rps choice(rock, paper, scissors)", value=info5, inline=True)
    info6 = "Play tictactoe with your friends"
    em.add_field(name="!tictactoe member member", value=info6, inline=True)
    info7 = "Donate 10 gems to another member (only available for Admins and you can not donate yourself gems)"
    em.add_field(name="!donate member", value=info7, inline=True)
    info8 = "Play rock paper scissors"
    em.add_field(name="!rps choice(rock, paper, scissors)", value=info8, inline=True)
    info9 = "Buy a role for a fixed amount ie(Admin-1000, Owner-10000)"
    em.add_field(name="!buy (role)", value=info9, inline=True)
    await ctx.send(embed=em)


@client.command()
async def rps(ctx, message):
    answer = message.lower()
    choices = ["rock", "paper", "scissors"]
    computer_answer = random.choice(choices)
    if answer not in choices:
        await ctx.send("That is not valid answer, please pick one from rock, paper or scissors!")
    else:
        if computer_answer == answer:
            await ctx.send(f"Tie! We both picked {answer}")
        if computer_answer == "rock":
            if answer == "paper":
                await ctx.send(f"You win! I picked {computer_answer}, You also got 50 coins for winning")
                users = await get_bank_data()
                user = ctx.author
                earnings = 50
                users[str(user.id)]["Coins"] += earnings
                with open("economy.json", "w") as f:
                    json.dump(users, f)
            if answer == "scissors":
                await ctx.send(f"You lose! I picked {computer_answer}, You lost 25 coins for losing")
                users = await get_bank_data()
                user = ctx.author
                earnings = 25
                users[str(user.id)]["Coins"] -= earnings
                with open("economy.json", "w") as f:
                    json.dump(users, f)
        if computer_answer == "paper":
            if answer == "rock":
                await ctx.send(f"You lose! I picked {computer_answer}, You lost 25 coins for losing")
                users = await get_bank_data()
                user = ctx.author
                earnings = 25
                users[str(user.id)]["Coins"] -= earnings
                with open("economy.json", "w") as f:
                    json.dump(users, f)
            if answer == "scissors":
                await ctx.send(f"You win! I picked {computer_answer}, You also got 50 coins for winning")
                users = await get_bank_data()
                user = ctx.author
                earnings = 50
                users[str(user.id)]["Coins"] += earnings
                with open("economy.json", "w") as f:
                    json.dump(users, f)
        if computer_answer == "scissors":
            if answer == "paper":
                await ctx.send(f"You lose! I picked {computer_answer}, You lost 25 coins for losing")
                users = await get_bank_data()
                user = ctx.author
                earnings = 25
                users[str(user.id)]["Coins"] -= earnings
                with open("economy.json", "w") as f:
                    json.dump(users, f)
            if answer == "rock":
                await ctx.send(f"You win! I picked {computer_answer}, You also got 50 coins for winning")
                users = await get_bank_data()
                user = ctx.author
                earnings = 50
                users[str(user.id)]["Coins"] += earnings
                with open("economy.json", "w") as f:
                    json.dump(users, f)


@client.command()
async def buy(ctx, role=None):
    member = ctx.author
    users = await get_bank_data()
    user = ctx.author
    wallet_amt = users[str(user.id)]["Coins"]
    if role.lower() == "admin":
        if wallet_amt > 1000:
            money_req = 1000
            users[str(user.id)]["Coins"] -= money_req

            with open("economy.json", "w") as f:
                json.dump(users, f)
            var = discord.utils.get(ctx.guild.roles, name=role)
            await member.add_roles(var)
            await ctx.channel.send("Successfully gave Admin" + " role " + "to " + ctx.author.name)
        else:
            await ctx.channel.send("You don't have enough coins for that.")
    if role.lower() == "owner":
        if wallet_amt > 10000:
            money_req = 10000
            users[str(user.id)]["Coins"] -= money_req

            with open("economy.json", "w") as f:
                json.dump(users, f)
            var = discord.utils.get(ctx.guild.roles, name="Owner")
            await member.add_roles(var)
            await ctx.channel.send("Successfully gave Owner" + " role " + "to " + ctx.author.name)
            await ctx.channel.send("Congrats" + ctx.author.name + " is now an owner")
        else:
            await ctx.channel.send("You don't have enough coins for that.")


@client.command()
async def balance(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    wallet_amt = users[str(user.id)]["Coins"]
    bank_amt = users[str(user.id)]["Gems"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance", color=discord.Color.red())
    em.add_field(name="Coins", value=wallet_amt)
    em.add_field(name="Gems", value=bank_amt)
    await ctx.send(embed=em)


@client.command()
async def convert(ctx, amount=0):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()
    gem_amt = users[str(user.id)]["Gems"]
    if amount <= gem_amt:
        new_amt = amount * 10
        users[str(user.id)]["Gems"] -= amount
        users[str(user.id)]["Coins"] += new_amt
        await ctx.send(f"Successfully converted {amount} gems into {new_amt} coins!")
        with open("economy.json", "w") as f:
            json.dump(users, f)
    elif amount > gem_amt:
        await ctx.send("You don't have that much Gems to convert in your account!")


@client.command()
@has_permissions(manage_roles=True)
async def donate(ctx, member: discord.Member):
    await open_account(member)
    if ctx.author == member:
        await ctx.send("You can't give yourself Gems!")
    else:
        user = member.id
        users = await get_bank_data()
        amt = 10
        await ctx.send(f"{ctx.author} gave {member} [10] Gems as an appreciation")
        users[str(user)]["Gems"] += amt
        with open("economy.json", "w") as f:
            json.dump(users, f)


@donate.error
async def donate(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have required roles(Admin,Owner) to do that!")


@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(f"Someone took away {earnings} coins from you!That's what you get for using this command")

    users[str(user.id)]["Coins"] -= earnings

    with open("economy.json", "w") as f:
        json.dump(users, f)


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Coins"] = 0
        users[str(user.id)]["Gems"] = 0

    with open("economy.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("economy.json", "r") as f:
        users = json.load(f)

    return users


@client.command()
async def level(ctx):
    global ranking
    await open_account_level(ctx.author)

    users = await get_level_data()

    class LeaderBoardPosition:
        def __init__(self, id, exp):
            self.id = id
            self.exp = exp

    leaderboard = []

    for user in users:
        leaderboard.append(LeaderBoardPosition(user, users[user]["Exp"]))

    top = sorted(leaderboard, key=lambda x: x.exp, reverse=True)

    for user in top:
        if user.id == str(ctx.author.id):
            ranking = top.index(user) + 1

    exp_level = users[str(ctx.author.id)]["Exp"]
    bank_amt = users[str(ctx.author.id)]["Level"]

    embed = discord.Embed(title=f"{ctx.author.name}'s Balance",
                          color=discord.Color.red())

    embed.add_field(name="EXP", value=exp_level, inline=True)
    embed.add_field(name="Level", value=bank_amt, inline=True)
    embed.add_field(name="Rank", value=ranking, inline=True)

    await ctx.send(embed=embed)


async def add_experience(users, user, exp):
    users[f'{user.id}']['Exp'] += exp


async def level_up(users, user, message):
    with open('users.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['Exp']
    lvl_start = users[f'{user.id}']['Level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['Level'] = lvl_end


async def open_account_level(user):
    users = await get_level_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Exp"] = 0
        users[str(user.id)]["Level"] = 0
        users[str(user.id)]["Rank"] = 0

    with open("users.json", "w") as f:
        json.dump(users, f)
    return True


async def get_level_data():
    with open("users.json", "r") as f:
        users = json.load(f)

    return users


@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                    if mark == ':o2:':
                        await ctx.send(f"{player2} won and also got 100 coins!")
                        await open_account(player2)
                        users = await get_bank_data()
                        earnings = 100
                        user = player2.id
                        users[str(user)]["Coins"] += earnings
                        with open("economy.json", "w") as f:
                            json.dump(users, f)
                    if mark == ':regional_indicator_x:':
                        await ctx.send(f"{player1} won and also got 100 coins")
                        user = player1.id
                        await open_account(player1)
                        users = await get_bank_data()
                        earnings = 100
                        users[str(user)]["Coins"] += earnings
                        with open("economy.json", "w") as f:
                            json.dump(users, f)
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


async def give_money():
    pass


with open('token.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
client.run(token)
