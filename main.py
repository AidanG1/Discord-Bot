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
        type=discord.ActivityType.listening, name="^help"))


@bot.event
async def on_message(message):
    if message.content == 'test Rice bot':
        await message.channel.send('Testing 1 2 3!')
    if message.content.lower() == 'poggers':
        if message.author != bot.user:
            await message.channel.send(message.content)
    if 'bruh' in message.content.lower():
        author = message.author
        if author != bot.user:
            db_name = 'bruh_' + str(author).replace('#','')
            if len(db.prefix(db_name)) > 0:
                db[db_name] += 1
            else:
                db[db_name] = 1
            if db['bruh_counter_enabled'] == True:
                await message.channel.send(f'Bruh counter for {author} is now {db[db_name]}')
    await bot.process_commands(message)


@bot.event
async def on_command(ctx):
    if len(db.prefix(ctx.command)) > 0:
        db[ctx.command] += 1
    else:
        db[ctx.command] = 1

@bot.command(aliases=['nyt'])
async def nyt_popular(ctx):
    '''
    Get the real time most popular New York Times article
    '''
    message = await ctx.send('loading...')
    r = requests.get('https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=' + os.getenv('nyt-key'))
    result = r.json()['results'][0]
    embed = discord.Embed(title=result['title'],
                          url=result['url'],
                          description=result['abstract'],
                          color=discord.Color.green())
    embed.set_image(url=result['media'][0]['media-metadata'][2]['url'])
    await ctx.send(embed=embed)
    await message.delete()


@bot.command(aliases=['cfrq', 'frq'])
async def command_frequency(ctx):
    '''
    Get the amount of times that each command has been run
    '''
    keys = db.keys()
    key_list = []
    for key in keys:
        if 'bruh_' not in key and '#' not in key:
            key_list.append([key, db[key]])
    key_list = sorted(key_list, key=lambda x: x[1], reverse=True)
    command = ''
    times_run = ''
    for key in key_list[0:10]:
        command += f"{key[0]}\n"
        times_run += f"{key[1]}\n"
    embed = discord.Embed(title='Most Run Commands',color=discord.Color.gold())
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
    elif indic_type.lower() in [
            'yragopricechangepct', 'pctch', 'changepct', '1yr', '1yrchange',
            '1y'
    ]:
        cnbc_type = 'yragopricechangepct'
    elif indic_type.lower() in ['fpe', 'forwardpe', 'forward_pe']:
        cnbc_type = 'fpe'
    elif indic_type.lower() in ['pe', 'price_earnings']:
        cnbc_type = 'pe'
    ticker = random.choice(tickers)
    r = requests.get(
        'https://quote.cnbc.com/quote-html-webservice/quote.htm?output=json&requestMethod=quick&symbols='
        + ticker)
    company_name = r.json()['QuickQuoteResult']['QuickQuote']['onAirName']
    value = float(r.json()['QuickQuoteResult']['QuickQuote']['FundamentalData']
                  [cnbc_type])
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
    await ctx.send(
        f'Guess the current {indic_type} of {company_name} ({ticker}) (type ^g and then the value to guess)'
    )


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
        pct_off = abs(100 * (guess - bot.value) / bot.value)
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
    embed = discord.Embed(title=result['title'],
                          url=result['href'],
                          description=result['ingredients'],
                          color=discord.Color.blue())
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
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name=phrase))
    elif type[0].lower() in ['g', 'p']:
        await bot.change_presence(activity=discord.Game(name=phrase))
    else:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=phrase))

@bot.command(aliases=['bce'])
@commands.has_role('Admins')
async def bruhCounter_enabled(ctx):
    '''
    Admin only command to change whether the bruh counter is enabled
    '''
    if len(db.prefix('bruh_counter_enabled')) == 0:
        db['bruh_counter_enabled'] = True
    else:
        db['bruh_counter_enabled'] =  not db['bruh_counter_enabled']
        await ctx.send(f"The bruh counter is now {db['bruh_counter_enabled']}")

@bot.command(aliases=['bc'])
async def bruhCount(ctx):
    '''
    Get bruh count
    '''
    message = await ctx.send('loading...')
    keys = db.keys()
    filtered_keys = [key for key in keys if key[0:5]=='bruh_']
    bruh_keys = []
    for i in range(len(filtered_keys)):
        if '#' not in filtered_keys[i]:
            bruh_keys.append([filtered_keys[i], db[filtered_keys[i]]])
            bruh_keys = sorted(bruh_keys, key=lambda x: x[1], reverse=True)[0:10]
    user = ''
    bruhs = ''
    for key in bruh_keys:
        user += f"{key[0][5:]}\n"
        bruhs += f"{key[1]}\n"
    embed = discord.Embed(title='User Bruh Count',color=discord.Color.gold())
    embed.add_field(name='User', value=user, inline=True)
    embed.add_field(name='Bruh Count', value=bruhs, inline=True)
    await ctx.send(embed=embed)
    await message.delete()
        
        

@bot.command(aliases=['chuck', 'norris'])
async def chuck_norris(ctx):
    '''
    Random Chuck Norris fact
    '''
    r = requests.get('https://api.chucknorris.io/jokes/random')
    result = r.json()
    if len(result['value']) > 255:
        embed = discord.Embed(title='Chuck Norris Fact',
                              description=result['value'],
                              color=discord.Color.purple())
    else:
        embed = discord.Embed(title=result['value'],
                              color=discord.Color.purple())
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
        embed = discord.Embed(title='Kanye West Quote',
                              description=quote,
                              color=discord.Color.green())
    else:
        embed = discord.Embed(title=quote, color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command(aliases=['apod', 'space', 'space_picture'])
async def astronomy_picture(ctx):
    '''
    NASA Astronomy picture of the day
    '''
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=' +
                     os.getenv('nasa-key'))
    result = r.json()
    embed = discord.Embed(
        title=result['title'],
        description=
        f"https://apod.nasa.gov/apod/astropix.html: {result['explanation']}",
        color=discord.Color.red())
    embed.set_image(url=result['url'])
    await ctx.send(embed=embed)


@bot.command(aliases=['cxkcd', 'rxkcd'])
async def recent_xkcd(ctx):
    '''
    Get the most recent xkcd
    '''
    r = requests.get('https://xkcd.com/info.0.json')
    result = r.json()
    embed = discord.Embed(title=f"{result['title']}: https://xkcd.com",
                          description=result['alt'],
                          color=discord.Color.teal())
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
    embed = discord.Embed(title=f"{result['title']}: https://xkcd.com/{result['num']}",
                          description=result['alt'],
                          color=discord.Color.dark_teal())
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
        embed = discord.Embed(title='Friends Quote',
                              description=quote,
                              color=discord.Color.green())
    else:
        embed = discord.Embed(title=quote, color=discord.Color.green())
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
        embed = discord.Embed(title='Taylor Swift Quote',
                              description=quote,
                              color=discord.Color.magenta())
    else:
        embed = discord.Embed(title=quote, color=discord.Color.magenta())
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
        await ctx.send(
            'For proper formatting visit: https://repl.it/@AidanGerber/Discord-Bot#readme.md'
        )


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

@bot.command()
async def stock_outlook(ctx, stock):
    '''
    Get an outlook for a stock. The outlook is randomly selected
    '''
    phrases = [
        f'{stock} looks very overpriced',
        f'{stock} is a great value right now',
        f'{stock} to the moon',
        f'There are bulls, there are bears, and then there are absolute failures which is what you are if you buy {stock}',
        f'{stock} is not stonks',
        f'{stock} is the next GameStop',
        f"Can't stop won't stop {stock}stock",
        f"I can't wait to lose all of my money on {stock}",
        f"Puts on {stock}",
        f"I wouldn't want {stock} if you paid me for it",
        f"I would rather buy puts on {stock} that put food on my table",
        f"If I didn't lose all my money on SHLD and BBI I would buy {stock}",
    ]
    await ctx.send('This is not financial advice: ' + random.choice(phrases))


@bot.command(aliases=['basketballstocks', 'basketball_stocks'])
async def bball(ctx, player):
    '''
    Get player price on basketballstocks.com using slug
    '''
    url = 'https://www.basketballstocks.com/api/players/' + player
    r = requests.get(url)
    result = r.json()
    await ctx.send(
        f"{result['name']}'s current price is ${result['current_price']}: https://basketballstocks.com/p/{result['slug']} ")

@bot.command(aliases=['ym', 'yomama', 'yomomma'])
async def yo_mama(ctx):
    '''
    Random yo mama joke. I didn't write these so some are offensive or nsfw
    '''
    url = 'https://raw.githubusercontent.com/rdegges/yomomma-api/master/jokes.txt'
    r = requests.get(url)
    result = r.text
    jokes = result.split('\n')
    joke = random.choice(jokes)
    while joke[0:18] == 'Yo mama is so dark':
        joke = random.choice(jokes)
    await ctx.send(joke)


@bot.command(aliases=['nbap'])
async def nba_player(ctx, *args):
    '''
    Get nba player advanced stats by name
    '''
    phrase = ''
    for arg in args:
        phrase += arg.lower() + '-'
    phrase = phrase[:-1]
    url = 'https://projects.fivethirtyeight.com/2021-nba-player-projections/' + phrase + '.json'
    r = requests.get(url)
    result = r.json()
    result = result['player_stats']
    name = result['player']
    team = result['team']
    url = result['headshot_url']
    category = result['category']
    current_year = datetime.date.today().year - 1 # doesn't actually get current nba season
    combined_war_per_82 = result['war_mean_' + str(current_year) + '_BL']
    embed = discord.Embed(title=name, description=f'Team: {team}\n Status: {category}\nLast Year War Per 82: {round(float(combined_war_per_82), 2)}', color=discord.Color.purple())
    embed.set_thumbnail(url=url)
    await ctx.send(embed=embed)


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
    phrase = ''''''
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
    embed = discord.Embed(title='Reactions',
                          description=reactions,
                          color=discord.Color.orange())
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
    count = int(count)
    if count < 3:
        count = 3
    headers = {
        'User-Agent': 'Discord Bot/0.1 requests',
    }
    r = requests.get(url, headers=headers)
    articles = r.json()['items'][0]['articles']
    pages = ['']
    views = ['']
    i = 0
    for article in articles[:count]:
        if len(pages[i]) + len(views[i]) > 1024:
            i += 1
            pages.append('')
            views.append('')
        if article['article'] not in ['Main_Page', 'Special:Search']:
            pages[i] += f"[{article['article']}]({'https://wikipedia.org/wiki/' + article['article']})\n"
            views[i] += f"{article['views']:,}\n"

    with open('slurs_to_ban.txt') as f:
        text = f.read()
        embeds = []
        for index in pages:
            embeds.append(discord.Embed(title=title, color=discord.Color.blurple()))
        words_to_ban = text.split(',')
        for word in words_to_ban:
            for page in pages:
                word = word.strip()
                wtr = word[0]
                for i in range(len(word) - 1):
                    wtr += '*'
                page = page.replace(word, wtr, 1)
                word = word.title()
                wtr = word[0]
                for i in range(len(word) - 1):
                    wtr += '*'
                page = page.replace(word, wtr, 1)
        for i in range(len(pages)):
            embeds[i].add_field(name='Page Title', value=pages[i], inline=True)
            embeds[i].add_field(name='Views', value=views[i], inline=True)
        parts = len(embeds)
        for i in range(len(embeds)):
            embeds[i].title += f', part {i+1} of {parts}'
        return embeds


@bot.command(aliases=['wiki'])
async def wikipedia_most_viewed(ctx, count='15'):
    '''
    Get the most visited wikipedia pages yesterday
    '''
    today = datetime.datetime.today() - datetime.timedelta(hours=32)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}"
    embeds = get_wiki(
        ctx, url,
        f"Most Viewed Wikipedia Pages On {today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}",
        count)
    for embed in embeds:
        await ctx.send(embed=embed)


@bot.command(aliases=['wikim'])
async def wikipedia_most_monthly(ctx, count='15'):
    '''
    Get the most visited wikipedia pages last month
    '''
    today = datetime.datetime.today() - datetime.timedelta(
        hours=32) - dateutil.relativedelta.relativedelta(months=1)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/all-days"
    embeds = get_wiki(
        ctx, url,
        f"Most Viewed Wikipedia Pages Over {today.strftime('%Y')}/{today.strftime('%m')}",
        count)
    for embed in embeds:
        await ctx.send(embed=embed)

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send("That command does not exist. Use ^help to get a list of commands.")



keep_alive()
bot.run(TOKEN)
