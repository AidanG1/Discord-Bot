import discord, os, random, requests, datetime
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
from wyr import questions
from ticker_list import tickers
from replit import db
import dateutil.relativedelta

load_dotenv()

help_command = commands.DefaultHelpCommand(no_category='Commands')

bot = commands.Bot(command_prefix='^', help_command=help_command)

TOKEN = os.getenv('TOKEN')


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="a movie"))
    
@bot.event
async def on_message(message):
    if message.content == 'test Rice bot':
        await message.channel.send('Testing 1 2 3!')
    if message.content == 'poggers':
        if message.author != bot.user:
            await message.channel.send('poggers')
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    if len(db.prefix(ctx.command))>0:
        db[ctx.command] += 1
    else:
        db[ctx.command] = 1

@bot.command(aliases=['cfrq', 'frq'])
async def command_frequency(ctx):
    '''
    Get the amount of times that each command has been run
    '''
    keys = db.keys()
    key_list = []
    for key in keys:
        key_list.append([key, db[key]])
    key_list = sorted(key_list, key=lambda x: x[1], reverse=True)
    command = ''
    times_run = ''
    for key in key_list[0:10]:
        command += f"{key[0]}\n"
        times_run += f"{key[1]}\n"
    embed = discord.Embed(title='Most Run Commands')
    embed.add_field(name='Command', value=command, inline=True)
    embed.add_field(name='Times Run', value=times_run, inline=True)
    await ctx.send(embed=embed)

bot.current_trivia_answer = ''

@bot.command(aliases=['trivia_question', 'triv'])
async def trivia(ctx):
    '''
    Get a random trivia question
    '''
    r = requests.get('http://jservice.io/api/random')
    bot.current_trivia_answer = r.json()[0]['answer']
    print(bot.current_trivia_answer)
    await ctx.send(r.json()[0]['question'])

@bot.command(aliases=['a'])
async def answer(ctx, *args):
    '''
    Answer a trivia question
    '''
    answer = ''
    for arg in args:
        answer += arg + ' '
    answer = answer.strip()
    if answer.lower() == bot.current_trivia_answer.lower():
        await ctx.send('Correct!')
    elif answer.lower() in ['igu', 'i give up']:
        await ctx.send(bot.current_trivia_answer)
    else:
        await ctx.send('Incorrect')

@bot.command()
async def randrange(ctx, low_number, high_number):
    '''
    Get a random number between two integers
    '''
    try:
        low_num = int(low_number)
        high_num = int(high_number)
        if low_num > high_num:
            low_num, high_num = high_num, low_num
        if low_num == high_num:
            await ctx.send('Your two numbers cannot be the same')
        else:
            await ctx.send(
                f'Your number is {random.randrange(low_num, high_num)}')
    except TypeError:
        await ctx.send('Enter an integer')

@bot.command(aliases=['sg'])
async def stock_guess(ctx, indic_type):
    '''
    The bot picks a random stock and you guess the value of 1yr change,market cap, pe, or forward pe
    '''
    if indic_type.lower() in ['cap', 'mcap', 'market_cap', 'mktcap']:
        cnbc_type = 'mktcap'
    elif indic_type.lower() in ['yragopricechangepct', 'pctch', 'changepct', '1yr', '1yrchange', '1y']:
        cnbc_type = 'yragopricechangepct'
    elif indic_type.lower() in ['fpe', 'forwardpe', 'forward_pe']:
        cnbc_type = 'fpe'
    elif indic_type.lower() in ['pe', 'price_earnings']:
        cnbc_type = 'pe'
    ticker = random.choice(tickers)
    r = requests.get('https://quote.cnbc.com/quote-html-webservice/quote.htm?output=json&requestMethod=quick&symbols=' + ticker)
    company_name = r.json()['QuickQuoteResult']['QuickQuote']['onAirName']
    value = float(r.json()['QuickQuoteResult']['QuickQuote']['FundamentalData'][cnbc_type])
    value_range = []
    value_range.append(value * 0.94)
    value_range.append(value)
    value_range.append(value * 1.06)
    bot.value_range = value_range
    bot.value = value
    bot.company_name = company_name
    bot.indic_type = indic_type
    bot.stock_guesses = []
    bot.ticker = ticker
    await ctx.send(f'Guess the current {indic_type} of {company_name} ({ticker}) (type ^g and then the value to guess)')


@bot.command(aliases=['g'])
async def guess(ctx, value):
    '''
    Answer a stock question
    '''
    message = f'The value of {bot.indic_type} for {bot.company_name} ({bot.ticker}) is {bot.value}'
    if value in ['igu', 'i_give_up']:
        await ctx.send('Answer: ' + message)
        return
    guess = float(value)
    bot.stock_guesses.append(guess)
    if guess > bot.value_range[0] and guess < bot.value_range[2]:
        await ctx.send('Correct! ' + message)
    else:
        pct_off = abs(100 * (guess-bot.value)/bot.value)
        if pct_off > 100:
            closeness = 'extremely far.'
        elif pct_off > 75:
            closeness = 'very far.'
        elif pct_off > 50:
            closeness = 'far.'
        elif pct_off > 50:
            closeness = 'far.'
        elif pct_off > 25:
            closeness = 'somewhat close.'
        elif pct_off > 15:
            closeness = 'close.'
        elif pct_off > 10:
            closeness = 'very close.'
        elif pct_off > 6:
            closeness = 'extremely close.'
        await ctx.send('Incorrect. You are ' + closeness)

@bot.command(aliases=['cook'])
async def recipe(ctx, query, *args):
    '''
    Find a recipe by listing ingredients and what you want to make
    '''
    phrase = ''
    for arg in args:
        phrase += arg + ','
    message = await ctx.send('loading...')
    r = requests.get(f'http://www.recipepuppy.com/api/?i={phrase}&q={query}')
    result = random.choice(r.json()['results'])
    embed=discord.Embed(title=result['title'], url=result['href'], description=result['ingredients'], color=discord.Color.blue())
    if result['thumbnail'] != '':
        embed.set_thumbnail(url=result['thumbnail'])
    await ctx.send(embed=embed)
    await message.delete()


@bot.command(aliases=['cp'])
@commands.has_role('Admins')
async def change_presence(ctx, type, *args):
    '''
    Admin only command to change bot presence
    '''
    phrase = ''
    for arg in args:
        phrase += arg + ' '
    phrase = phrase.title()
    if type[0].lower() == 'l':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=phrase))
    elif type[0].lower() in ['g', 'p']:
        await bot.change_presence(activity=discord.Game(name=phrase))
    else:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=phrase))

@bot.command(aliases=['chuck', 'norris'])
async def chuck_norris(ctx):
    '''
    Random Chuck Norris fact
    '''
    r = requests.get('https://api.chucknorris.io/jokes/random')
    result = r.json()
    if len(result['value']) > 255:
        embed=discord.Embed(title='Chuck Norris Fact',description=result['value'], color=discord.Color.purple())
    else:
         embed=discord.Embed(title=result['value'], color=discord.Color.purple())
    embed.set_thumbnail(url=result['icon_url'])
    await ctx.send(embed=embed)

@bot.command(aliases=['kanye'])
async def kanye_west(ctx):
    '''
    Random Kanye West Quote 
    '''
    r = requests.get('https://api.kanye.rest/')
    result = r.json()
    quote = f'''"{result['quote']}" - Kanye West'''
    if len(quote) > 255:
        embed=discord.Embed(title='Kanye West Quote', description=quote, color=discord.Color.green())
    else:
        embed=discord.Embed(title=quote, color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(aliases=['apod', 'space', 'space_picture'])
async def astronomy_picture(ctx):
    '''
    NASA Astronomy picture of the day
    '''
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + os.getenv('nasa-key'))
    result = r.json()
    embed=discord.Embed(title=result['title'], description=f"https://apod.nasa.gov/apod/astropix.html: {result['explanation']}",color=discord.Color.red())
    embed.set_image(url=result['url'])
    await ctx.send(embed=embed)

@bot.command(aliases=['cxkcd', 'rxkcd'])
async def recent_xkcd(ctx):
    '''
    Get the most recent xkcd
    '''
    r = requests.get('https://xkcd.com/info.0.json')
    result = r.json()
    embed=discord.Embed(title=result['title'], description= result['alt'],color=discord.Color.dark_teal())
    embed.set_image(url=result['img'])
    await ctx.send(embed=embed)

@bot.command(aliases=['xkcd'])
async def random_xkcd(ctx):
    '''
    Get a random xkcd
    '''
    r = requests.get('https://xkcd.com/info.0.json')
    rand_num = random.randrange(1, r.json()['num'])
    r = requests.get(f'https://xkcd.com/{rand_num}/info.0.json')
    result = r.json()
    embed=discord.Embed(title=result['title'], description= result['alt'],color=discord.Color.dark_teal())
    embed.set_image(url=result['img'])
    await ctx.send(embed=embed)
          
@bot.command(aliases=['num', 'num_fact', 'number'])
async def number_fact(ctx, number):
    '''
    Get a fact about a number
    '''
    r = requests.get('http://numbersapi.com/' + number)
    result = r.text
    await ctx.send(result)

@bot.command(aliases=['bp'])
async def bread_pun(ctx):
    '''
    Get a random bread pun
    '''
    r = requests.get('https://my-bao-server.herokuapp.com/api/breadpuns')
    result = r.text
    await ctx.send(result)

@bot.command(aliases=['fortune_cookie'])
async def advice(ctx):
    '''
    Get fortune-cookie-esque advice
    '''
    r = requests.get('https://api.adviceslip.com/advice')
    result = r.json()['slip']['advice']
    await ctx.send(result)

@bot.command(aliases=['fq'])
async def friends_quote(ctx):
    '''
    Random Friends Quote
    '''
    r = requests.get('https://friends-quotes-api.herokuapp.com/quotes/random')
    result = r.json()
    quote = f'''"{result['quote']}" - {result['character']}'''
    if len(quote) > 255:
        embed=discord.Embed(title='Friends Quote', description=quote, color=discord.Color.green())
    else:
        embed=discord.Embed(title=quote, color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(aliases=['tsq'])
async def taylor_swift_quote(ctx):
    '''
    Random Taylor Swift Quote
    '''
    r = requests.get('https://api.taylor.rest/')
    result = r.json()
    quote = f'''"{result['quote']}" - Taylor Swift'''
    if len(quote) > 255:
        embed=discord.Embed(title='Taylor Swift Quote', description=quote, color=discord.Color.green())
    else:
        embed=discord.Embed(title=quote, color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(aliases=['chess'])
async def chess_stats(ctx, username):
    '''
    Get chess.com info, include username with command
    '''
    url = 'https://api.chess.com/pub/player/' + username
    r = requests.get(url + '/stats')
    result = r.json()
    types = ''
    ratings = ''
    chess_types = ['chess_rapid', 'chess_bullet', 'chess_blitz', 'chess_daily']
    no_types = True
    for chess_type in chess_types:
        if chess_type in result:
            types += chess_type + '\n'
            ratings += str(result[chess_type]['last']['rating']) + '\n'
            no_types = False
    if no_types:
        types = 'No game types played'
        ratings = 'N/A'
    embed = discord.Embed(title=f'Ratings of {username}')
    embed.add_field(name='Type', value=types, inline=True)
    embed.add_field(name='Rating', value=ratings, inline=True)
    await ctx.send(embed=embed)


@bot.command(aliases=['get_ping'])
async def ping(ctx):
    '''
    Get bot ping
    '''
    latency = bot.latency
    await ctx.send(f'Latency: {round(latency, 4)} seconds')


@bot.command(aliases=['code'])
async def get_code(ctx):
    '''
    Get the code for this bot
    '''
    await ctx.send('https://repl.it/@AidanGerber/Discord-Bot#main.py')
 

@bot.command(aliases=['aliases', 'alias', 'docs'])
async def get_aliases(ctx):
    '''
    Get a list of command aliases
    '''
    with open('readme.md') as f:
        text = f.read()
        messages = ['']
        for character in text:
            if len(messages[-1]) < 2000:
                messages[-1] += character
            else:
                messages.append(character)
        for message in messages:
            await ctx.send(message)
        await ctx.send('For proper formatting visit: https://repl.it/@AidanGerber/Discord-Bot#readme.md')

@bot.command()
async def yang(ctx):
    '''
    yin
    '''
    await ctx.send('yin')


@bot.command()
async def yin(ctx):
    '''
    yang
    '''
    await ctx.send('yang')


@bot.command()
async def pong(ctx):
    '''
    ping
    '''
    await ctx.send('ping')


@bot.command(aliases=['basketballstocks', 'basketball_stocks'])
async def bball(ctx, player):
    '''
    Get player price on basketballstocks.com using slug
    '''
    url = 'https://www.basketballstocks.com/api/players/' + player
    r = requests.get(url)
    result = r.json()
    await ctx.send(
        f"{result['name']}'s current price is ${result['current_price']}")


@bot.command(aliases=['ai_text_gen', 'ai_text_generation', 'ai'])
async def text_gen(ctx, *args):
    '''
    Generate a paragraph from a sentence or phrase using AI
    '''
    phrase = ''
    for arg in args:
        phrase += arg + ' '
    message = await ctx.send('loading...')
    r = requests.post("https://api.deepai.org/api/text-generator",
                      data={
                          'text': phrase,
                      },
                      headers={'api-key': os.getenv('api-key')})
    await ctx.send(r.json()['output'])
    await message.delete()

@bot.command(aliases=['sentiment', 'emotion', 'feeling', 'feel'])
async def sentiment_analysis(ctx, *args):
    '''
    Sentiment analysis of text
    '''
    phrase = ''
    for arg in args:
        phrase += arg + ' '
    message = await ctx.send('loading...')
    r = requests.post("https://api.deepai.org/api/sentiment-analysis",
                      data={
                          'text': phrase,
                      },
                      headers={'api-key': os.getenv('api-key')})
    await ctx.send(r.json()['output'])
    await message.delete()

@bot.command(aliases=['react', 'reaction_images'])
async def trendy_reactions(ctx):
    '''
    Get a list of classic reaction photos
    '''
    reactions = ''
    reactions += 'https://cdn.discordapp.com/attachments/787158737680597002/809995223261773864/20e.jpg' + '\nhttps://i.kym-cdn.com/photos/images/newsfeed/000/995/030/65e.jpg'
    embed=discord.Embed(title='Reactions', description=reactions, color=discord.Color.orange())
    await ctx.send(embed=embed)

def random_question(remove_list):
    question = random.choice(questions)
    while question['id'] in remove_list:
        question = random.choice(questions)
    return question


@bot.command(aliases=['wyr'])
async def would_you_rather(ctx):
    '''
    Get a would you rather
    '''

    message = await ctx.send(random_question([])['question'])
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')


@bot.command(aliases=['wyrl', 'wyrx'])
async def would_you_rather_list(ctx, remove_list):
    '''
    Get a would you rather and exclude questions from a list
    '''
    remove_list = list(remove_list)
    question = random_question(remove_list)
    message = await ctx.send(question['question'])
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    rl = [question['id']]
    number = ''
    for item in remove_list:
        try:
            int(item)
            number += item
        except ValueError:
            if number != '':
                rl.append(int(number))
            number = ''
    remove_list.append(question['id'])
    await ctx.send('^wyrl ' + str(rl).replace(' ', ''))

def get_wiki(ctx, url, title, count):
    headers = {
        'User-Agent': 'Discord Bot/0.1 requests',
    }
    r = requests.get(url, headers=headers)
    articles = r.json()['items'][0]['articles']
    page = ''
    views = ''
    for article in articles[0:count]:
        if article['article'] not in ['Main_Page', 'Special:Search']:
            page += f"[{article['article']}]({'https://wikipedia.org/wiki/' + article['article']})\n"
            views += f"{article['views']:,}\n"

    with open('slurs_to_ban.txt') as f:
        text = f.read()
        embed = discord.Embed(title=title)
        words_to_ban = text.split(',')
        for word in words_to_ban:
            word = word.strip()
            wtr = word[0]
            for i in range(len(word) - 1):
                wtr += '*'
            page = page.replace(word,  wtr, 1)
            word = word.title()
            wtr = word[0]
            for i in range(len(word) - 1):
                wtr += '*'
            page = page.replace(word, wtr, 1)
        embed.add_field(name='Page Title', value=page, inline=True)
        embed.add_field(name='Views', value=views, inline=True)
        return embed


@bot.command(aliases=['wiki'])
async def wikipedia_most_viewed(ctx, count='15'):
    '''
    Get the most visited wikipedia pages yesterday
    '''
    today = datetime.datetime.today() - datetime.timedelta(hours=32)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}"
    count = int(count)
    embed = get_wiki(ctx, url, f"Most Viewed Wikipedia Pages Over {today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}", count)
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send('Message too long to send')

@bot.command(aliases=['wikim'])
async def wikipedia_most_monthly(ctx, count='15'):
    '''
    Get the most visited wikipedia pages last month
    '''
    today = datetime.datetime.today() - datetime.timedelta(hours=32) - dateutil.relativedelta.relativedelta(months=1)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/all-days"
    count = int(count)
    embed = get_wiki(ctx, url, f"Most Viewed Wikipedia Pages Over {today.strftime('%Y')}/{today.strftime('%m')}", count)
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send('Message too long to send')

keep_alive()
bot.run(TOKEN)
