import discord, os, random, requests, datetime
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive

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
    await bot.process_commands(message)

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
    embed=discord.Embed(title=result['title'], description= result['explanation'],color=discord.Color.red())
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
    questions = [
        {
            'question':
            'Would you rather go into the past and meet your ancestors or go into the future and meet your great-great grandchildren?',
            'id': 1
        },
        {
            'question': 'Would you rather have more time or more money?',
            'id': 2
        },
        {
            'question':
            'Would you rather have a rewind button or a pause button on your life?',
            'id': 3
        },
        {
            'question':
            'Would you rather be able to talk with the animals or speak all foreign languages?',
            'id': 4
        },
        {
            'question':
            'Would you rather win the lottery or live twice as long?',
            'id': 5
        },
        {
            'question':
            'Would you feel worse if no one showed up to your wedding or to your funeral?',
            'id': 6
        },
        {
            'question':
            'Would you rather be without internet for a week, or without your phone?',
            'id': 7
        },
        {
            'question':
            'Would you rather meet George Washington, or the current President?',
            'id': 8
        },
        {
            'question': 'Would you rather lose your vision or your hearing?',
            'id': 9
        },
        {
            'question':
            'Would you rather work more hours per day, but fewer days or work fewer hours per day, but more days?',
            'id': 10
        },
        {
            'question':
            'Would you rather listen to music from the 70’s or music from today?',
            'id': 11
        },
        {
            'question':
            'Would you rather become someone else or just stay you?',
            'id': 12
        },
        {
            'question': 'Would you rather be Batman or Spiderman?',
            'id': 13
        },
        {
            'question':
            'Would you rather be stuck on a broken ski lift or in a broken elevator?',
            'id': 14
        },
        {
            'question':
            'For your birthday, would you rather receive cash or gifts?',
            'id': 15
        },
        {
            'question': 'Would you rather go to a movie or to dinner alone?',
            'id': 16
        },
        {
            'question':
            'Would you rather always say everything on your mind or never speak again?',
            'id': 17
        },
        {
            'question': 'Would you rather make a phone call or send a text?',
            'id': 18
        },
        {
            'question':
            'Would you rather read an awesome book or watch a good movie?',
            'id': 19
        },
        {
            'question':
            'Would you rather be the most popular person at work or school or the smartest?',
            'id': 20
        },
        {
            'question':
            'Would you rather put a stop to war or end world hunger?',
            'id': 21
        },
        {
            'question':
            'Would you rather spend the night in a luxury hotel room or camping surrounded by beautiful scenery?',
            'id': 22
        },
        {
            'question': 'Would you rather explore space or the ocean?',
            'id': 23
        },
        {
            'question':
            'Would you rather go deep sea diving or bungee jumping?',
            'id': 24
        },
        {
            'question':
            'Would you rather be a kid your whole life or an adult your whole life?',
            'id': 25
        },
        {
            'question':
            'Would you rather go on a cruise with friends or with your spouse?',
            'id': 26
        },
        {
            'question': 'Would you rather lose your keys or your cell phone?',
            'id': 27
        },
        {
            'question':
            'Would you rather eat a meal of cow tongue or octopus?',
            'id': 28
        },
        {
            'question':
            'Would you rather have x-ray vision or magnified hearing?',
            'id': 29
        },
        {
            'question': 'Would you rather work in a group or work alone?',
            'id': 30
        },
        {
            'question':
            'Would you rather be stuck on an island alone or with someone who talks incessantly?',
            'id': 31
        },
        {
            'question': 'Would you rather be too hot or too cold?',
            'id': 32
        },
        {
            'question':
            'When you’re old, would you rather die before or after your spouse?',
            'id': 33
        },
        {
            'question': 'Would you rather have a cook or a maid?',
            'id': 34
        },
        {
            'question':
            'Would you rather be the youngest or the oldest sibling?',
            'id': 35
        },
        {
            'question':
            'Would you rather get rich through hard work or through winning the lottery?',
            'id': 36
        },
        {
            'question':
            'Would you rather have a 10-hour dinner with a headstrong politician from an opposing party, or attend a 10-hour concert for a music group you detest?',
            'id': 37
        },
        {
            'question':
            'Would you rather be an Olympic gold medalist or a Nobel Peace Prize winner?',
            'id': 38
        },
        {
            'question': 'Would you rather have a desk job or an outdoor job?',
            'id': 39
        },
        {
            'question':
            'Would you rather live at the top of a tall NYC apartment building or at the top of a mountain?',
            'id': 40
        },
        {
            'question':
            'Would you rather have Rambo or The Terminator on your side?',
            'id': 41
        },
        {
            'question':
            'Would you rather be proposed to in private or in front of family and friends?',
            'id': 42
        },
        {
            'question':
            'Would you rather have to sew all your clothes or grow your own food?',
            'id': 43
        },
        {
            'question':
            'Would you rather hear the good news or the bad news first?',
            'id': 44
        },
        {
            'question':
            'Would you rather be your own boss or work for someone else?',
            'id': 45
        },
        {
            'question':
            'Would you rather have nosy neighbors or noisy neighbors?',
            'id': 46
        },
        {
            'question':
            'Would you rather be on a survival reality show or dating game show?',
            'id': 47
        },
        {
            'question': 'Would you rather be too busy or be bored?',
            'id': 48
        },
        {
            'question':
            'Would you rather watch the big game at home or live at the stadium.',
            'id': 49
        },
        {
            'question': 'Would you rather be too busy or be bored?',
            'id': 50
        },
        {
            'question':
            'Would you rather watch the big game at home or live at the stadium.',
            'id': 51
        },
        {
            'question':
            'Would you rather spend the day with your favorite athlete or you favorite movie star?',
            'id': 52
        },
        {
            'question':
            'Would you rather live where it is constantly winter or where it is constantly summer?',
            'id': 53
        },
        {
            'question':
            'Would you rather travel the US and see the sights in a motorhome or by plane?',
            'id': 54
        },
        {
            'question': 'Would you rather be a little late or way too early?',
            'id': 55
        },
        {
            'question':
            'Would you rather have an unlimited gift certificate to a restaurant or a clothing store?',
            'id': 56
        },
        {
            'question':
            'Would you rather date someone you met online or go on a blind date?',
            'id': 57
        },
        {
            'question':
            'Would you rather your kids wear a uniform to school or clothing of their choice?',
            'id': 58
        },
        {
            'question':
            'Would you rather have many good friends or one very best friend?',
            'id': 59
        },
        {
            'question':
            'Would you rather live in Antarctica or the Sahara Dessert?',
            'id': 60
        },
        {
            'question':
            'Would you rather be able to take back anything you say or hear every conversation around you?',
            'id': 61
        },
        {
            'question': 'Would you rather be 4’5” or 7’7”?',
            'id': 62
        },
        {
            'question':
            'Would you rather be poor and work at a job you love, or rich and work at a job you hate?',
            'id': 63
        },
        {
            'question':
            'Would you rather have your flight delayed by 8 hours or lose your luggage?',
            'id': 64
        },
        {
            'question':
            'Would you rather be in your pajamas or a suit all day?',
            'id': 65
        },
        {
            'question':
            'Would you rather have your first child when you are 18 or 40?',
            'id': 66
        },
        {
            'question':
            'Would you rather be the star player on a losing basketball team or ride the bench on a winning one?',
            'id': 67
        },
        {
            'question':
            'Would you rather spend the next year exempt from all taxes or have a one-month paid vacation?',
            'id': 68
        },
        {
            'question':
            'Would you rather have the best house in a bad neighborhood or the worst house in a good neighborhood?',
            'id': 69
        },
        {
            'question':
            'Would you rather be filthy rich and live 400 years ago or be poor but live today?',
            'id': 70
        },
        {
            'question':
            'Would you rather be gossiped about or never talked about at all?',
            'id': 71
        },
        {
            'question': 'Would you rather end hunger or hatred?',
            'id': 72
        },
        {
            'question':
            'Would you rather be an unknown major league baseball player or a famous badminton star?',
            'id': 73
        },
        {
            'question':
            'Would you rather go without TV or junk food the rest of your life?',
            'id': 74
        },
        {
            'question':
            'Would you rather spend the day at an amusement park or lazing on the beach?',
            'id': 75
        },
        {
            'question':
            'Would you rather be fluent in all languages or be a master of every musical instrument?',
            'id': 76
        },
        {
            'question':
            'Would you rather sing a song in front of complete strangers or your closest friends?',
            'id': 77
        },
        {
            'question':
            'Would you rather own your own boat or your own plane?',
            'id': 78
        },
        {
            'question':
            'Would you rather meet the president of the United States or a movie star?',
            'id': 79
        },
        {
            'question':
            'Would you rather spend two weeks stuck in a psychiatric hospital or stuck in an airport?',
            'id': 80
        },
        {
            'question':
            'If you had to give up one thing for the rest of your life, would it be brushing your hair or brushing your teeth?',
            'id': 81
        },
        {
            'question':
            'Would you rather spend 20 years in prison and be exonerated as innocent or be put away for four years (despite your innocence) and be considered guilty forever?',
            'id': 82
        },
        {
            'question': 'Would you rather own a house or rent a residence?',
            'id': 83
        },
        {
            'question':
            'Would you rather be known as a one-hit wonder for a novel or a song?',
            'id': 84
        },
        {
            'question':
            'Would you rather take an action-packed European vacation or spend two weeks at the same Caribbean resort?',
            'id': 85
        },
        {
            'question':
            'Would you rather be a character in an action-packed thriller or a romantic comedy?',
            'id': 86
        },
        {
            'question': 'Would you rather be stuck on a train or a bus?',
            'id': 87
        },
        {
            'question':
            'Would you rather be a part of an arranged marriage or spend your life as a single person?',
            'id': 88
        },
        {
            'question':
            'Would you rather babysit a crying infant for a day or have an unwanted houseguest for a week?',
            'id': 89
        },
        {
            'question':
            'Would you rather be locked in an amusement park or a library?',
            'id': 90
        },
        {
            'question':
            'Would you rather sing like an opera star or cook like a gourmet chef?',
            'id': 91
        },
        {
            'question':
            'Would you rather have your debt forgiven or have guaranteed good health for a decade?',
            'id': 92
        },
        {
            'question':
            'Would you rather live the rest of your life as a monk or followed continuously by paparazzi?',
            'id': 93
        },
        {
            'question':
            'Would you rather be given a lifetime supply of delicious food or books?',
            'id': 94
        },
        {
            'question':
            'Would you rather be able to breath underwater or fly through the air?',
            'id': 95
        },
        {
            'question':
            'Would you rather be known for your intelligence or your good looks?',
            'id': 96
        },
        {
            'question':
            'Would you rather eat pizza or ice cream as the only food for eternity?',
            'id': 97
        },
        {
            'question': 'Would you rather mentally or physically never age?',
            'id': 98
        },
        {
            'question':
            'Would you rather change your eye color or your hair color?',
            'id': 99
        },
        {
            'question':
            'Would you rather have the details of your financial life or your love life be made public?',
            'id': 100
        },
        {
            'question':
            'Would you rather spend a year as a cop or a teacher in an inner-city neighborhood?',
            'id': 101
        },
        {
            'question':
            'Would you rather have a family of 12 children or never be able to have children at all?',
            'id': 102
        },
        {
            'question':
            'Would you rather the aliens that make first contact be robotic or organic?',
            'id': 103
        },
        {
            'question':
            'Would you rather lose the ability to read or lose the ability to speak?',
            'id': 104
        },
        {
            'question':
            'Would you rather have a golden voice or a silver tongue?',
            'id': 105
        },
        {
            'question':
            'Would you rather be covered in fur or covered in scales?',
            'id': 106
        },
        {
            'question':
            'Would you rather be in jail for a year or lose a year off your life?',
            'id': 107
        },
        {
            'question':
            'Would you rather always be 10 minutes late or always be 20 minutes early?',
            'id': 108
        },
        {
            'question':
            'Would you rather have one real get out of jail free card or a key that opens any door?',
            'id': 109
        },
        {
            'question':
            'Would you rather know the history of every object you touched or be able to talk to animals?',
            'id': 110
        },
        {
            'question':
            'Would you rather be married to a 10 with a bad personality or a 6 with an amazing personality?',
            'id': 111
        },
        {
            'question':
            'Would you rather be able to talk to land animals, animals that fly, or animals that live under the water?',
            'id': 112
        },
        {
            'question':
            'Would you rather have all traffic lights you approach be green or never have to stand in line again?',
            'id': 113
        },
        {
            'question':
            'Would you rather spend the rest of your life with a sailboat as your home or an RV as your home?',
            'id': 114
        },
        {
            'question':
            'Would you rather give up all drinks except for water or give up eating anything that was cooked in an oven?',
            'id': 115
        },
        {
            'question':
            'Would you rather be able to see 10 minutes into your own future or 10 minutes into the future of anyone but yourself?',
            'id': 116
        },
        {
            'question':
            'Would you rather have an easy job working for someone else or work for yourself but work incredibly hard?',
            'id': 117
        },
        {
            'question':
            'Would you rather be the first person to explore a planet or be the inventor of a drug that cures a deadly disease?',
            'id': 118
        },
        {
            'question':
            'Would you rather go back to age 5 with everything you know now or know now everything your future self will learn?',
            'id': 119
        },
        {
            'question':
            'Would you rather be able to control animals (but not humans) with your mind or control electronics with your mind?',
            'id': 120
        },
        {
            'question':
            'Would you rather have unlimited international first-class tickets or never have to pay for food at restaurants?',
            'id': 121
        },
        {
            'question':
            'Would you rather see what was behind every closed door or be able to guess the combination of every safe on the first try?',
            'id': 122
        },
        {
            'question':
            'Would you rather be an average person in the present or a king of a large country 2500 years ago?',
            'id': 123
        },
        {
            'question':
            'Would you rather be able to dodge anything no matter how fast it’s moving or be able to ask any three questions and have them answered accurately?',
            'id': 124
        },
        {
            'question':
            'Would you rather be forced to dance every time you heard music or be forced to sing along to any song you heard?',
            'id': 125
        },
        {
            'question':
            'Would you rather have all your clothes fit perfectly or have the most comfortable pillow, blankets, and sheets in existence?',
            'id': 126
        },
        {
            'question':
            'Would you rather 5% of the population have telepathy, or 5% of the population have telekinesis? You are not part of the 5% that has telepathy or telekinesis',
            'id': 127
        },
        {
            'question':
            'Would you rather be an unimportant character in the last movie you saw or an unimportant character in the last book you read?',
            'id': 128
        },
        {
            'question':
            'Would you rather move to a new city or town every week or never be able to leave the city or town you were born in?',
            'id': 129
        },
        {
            'question':
            'Would you rather be completely insane and know that you are insane or completely insane and believe you are sane?',
            'id': 130
        },
        {
            'question':
            'Would you rather travel the world for a year on a shoestring budget or stay in only one country for a year but live in luxury?',
            'id': 131
        },
        {
            'question':
            'Would you rather suddenly be elected a senator or suddenly become a CEO of a major company? (You won’t have any more knowledge about how to do either job than you do right now',
            'id': 132
        },
        {
            'question':
            'Would you rather live in virtual reality where you are all powerful or live in the real world and be able to go anywhere but not be able to interact with anyone or anything?',
            'id': 133
        },
        {
            'question':
            'Would you rather have whatever you are thinking to appear above your head for everyone to see or have absolutely everything you do live streamed for anyone to see?',
            'id': 134
        },
        {
            'question':
            'Would you rather be only able to watch the few movies with a Rotten Tomatoes score of 95-100% or only be able to watch the majority of movies with a Rotten Tomatoes score of 94% and lower?',
            'id': 135
        },
        {
            'question':
            'Would you rather wake up as a new random person every year and have full control of them for the whole year or once a week spend a day inside a stranger without having any control of them?',
            'id': 136
        },
        {
            'question':
            'Would you rather know how above or below average you are at everything or know how above or below average people are at one skill/talent just by looking at them?',
            'id': 137
        },
        {
            'question':
            'Would you rather live until you are 200 but look like you are 200 the whole time even though you are healthy or look like you are 25 all the way until you die at age 65?',
            'id': 138
        },
        {
            'question':
            'Would you rather be a reverse centaur or a reverse mermaid/merman?',
            'id': 139
        },
        {
            'question':
            'Would you rather your only mode of transportation be a donkey or a giraffe?',
            'id': 140
        },
        {
            'question':
            'Would you rather only be to use a fork (no spoon) or only be able to use a spoon (no fork)?',
            'id': 141
        },
        {
            'question':
            'Would you rather every shirt you ever wear be kind of itchy or only be able to use 1 ply toilet paper?',
            'id': 142
        },
        {
            'question':
            'Would you rather have edible spaghetti hair that regrows every night or sweat (not sweet) maple syrup?',
            'id': 143
        },
        {
            'question':
            'Would you rather have to read aloud every word you read or sing everything you say out loud?',
            'id': 144
        },
        {
            'question':
            'Would you rather wear a wedding dress/tuxedo every single day or wear a bathing suit every single day?',
            'id': 145
        },
        {
            'question':
            'Would you rather be unable to move your body every time it rains or not be able to stop moving while the sun is out?',
            'id': 146
        },
        {
            'question':
            'Would you rather have all dogs try to attack you when they see you or all birds try to attack you when they see you?',
            'id': 147
        },
        {
            'question':
            'Would you rather be compelled to high five everyone you meet or be compelled to give wedgies to anyone in a green shirt?',
            'id': 148
        },
        {
            'question':
            'Would you rather have skin that changes color based on your emotions or tattoos appear all over your body depicting what you did yesterday?',
            'id': 149
        },
        {
            'question':
            'Would you rather randomly time travel +/- 20 years every time you fart or teleport to a different place on earth (on land, not water) every time you sneeze?',
            'id': 150
        },
        {
            'question':
            'Would you rather there be a perpetual water balloon war going on in your city/town or a perpetual food fight?',
            'id': 151
        },
        {
            'question':
            'Would you rather have to fart loudly every time you have a serious conversation or have to burp after every kiss?',
            'id': 152
        },
        {
            'question':
            'Would you rather become twice as strong when both of your fingers are stuck in your ears or crawl twice as fast as you can run?',
            'id': 153
        },
        {
            'question':
            'Would you rather have everything you draw become real but be permanently terrible at drawing or be able to fly but only as fast as you can walk?',
            'id': 154
        },
        {
            'question':
            'Would you rather thirty butterflies instantly appear from nowhere every time you sneeze or one very angry squirrel appear from nowhere every time you cough?',
            'id': 155
        },
        {
            'question':
            'Would you rather vomit uncontrollably for one minute every time you hear the happy birthday song or get a headache that lasts for the rest of the day every time you see a bird (including in pictures or a video)?',
            'id': 156
        },
        {
            'question':
            'Would you rather eat a sandwich made from 4 ingredients in your fridge chosen at random or eat a sandwich made by a group of your friends from 4 ingredients in your fridge?',
            'id': 157
        },
        {
            'question':
            'Would you rather everyone be required to wear identical silver jumpsuits or any time two people meet and are wearing an identical article of clothing they must fight to the death?',
            'id': 158
        },
        {
            'question':
            'Would you rather be a famous director or a famous actor?',
            'id': 159
        },
        {
            'question':
            'Would you rather be a practicing doctor or a medical researcher?',
            'id': 160
        },
        {
            'question':
            'Would you rather live in a cave or live in a tree house?',
            'id': 161
        },
        {
            'question': 'Would you rather be able to control fire or water?',
            'id': 162
        },
        {
            'question':
            'Would you rather live without the internet or live without AC and heating?',
            'id': 163
        },
        {
            'question':
            'Would you rather be able to teleport anywhere or be able to read minds?',
            'id': 164
        },
        {
            'question':
            'Would you rather be unable to use search engines or unable to use social media?',
            'id': 165
        },
        {
            'question':
            'Would you rather be beautiful/handsome but stupid or intelligent but ugly?',
            'id': 166
        },
        {
            'question':
            'Would you rather be balding but fit or overweight with a full head of hair?',
            'id': 167
        },
        {
            'question':
            'Would you rather never be able to eat meat or never be able to eat vegetables?',
            'id': 168
        },
        {
            'question':
            'Would you rather have a completely automated home or a self-driving car?',
            'id': 169
        },
        {
            'question':
            'Would you rather be an amazing painter or a brilliant mathematician?',
            'id': 170
        },
        {
            'question':
            'Would you rather be famous but ridiculed or be just a normal person?',
            'id': 171
        },
        {
            'question':
            'Would you rather have a flying carpet or a car that can drive underwater?',
            'id': 172
        },
        {
            'question':
            'Would you rather never be stuck in traffic again or never get another cold?',
            'id': 173
        },
        {
            'question':
            'Would you rather have a bottomless box of Legos or a bottomless gas tank?',
            'id': 174
        },
        {
            'question':
            'Would you rather be forced to eat only spicy food or only incredibly bland food?',
            'id': 175
        },
        {
            'question':
            'Would you rather be a bowling champion or a curling champion?',
            'id': 176
        },
        {
            'question':
            'Would you rather be fantastic at riding horses or amazing at driving dirt bikes?',
            'id': 177
        },
        {
            'question':
            'Would you rather never be able to wear pants or never be able to wear shorts?',
            'id': 178
        },
        {
            'question':
            'Would you rather live the next 10 years of your life in China or Russia?',
            'id': 179
        },
        {
            'question':
            'Would you rather live on the beach or in a cabin in the woods?',
            'id': 180
        },
        {
            'question':
            'Would you rather be lost in a bad part of town or lost in the forest?',
            'id': 181
        },
        {
            'question':
            'Would you rather have a horrible short-term memory or a horrible long-term memory?',
            'id': 182
        },
        {
            'question':
            'Would you rather be completely invisible for one day or be able to fly for one day?',
            'id': 183
        },
        {
            'question':
            'Would you rather never be able to use a touchscreen or never be able to use a keyboard and mouse?',
            'id': 184
        },
        {
            'question':
            'Would you rather have unlimited sushi for life or unlimited tacos for life? (both are amazingly delicious and can be any type of sushi/taco you want)',
            'id': 185
        },
        {
            'question':
            'Would you rather get one free round trip international plane ticket every year or be able to fly domestic anytime for free?',
            'id': 186
        },
        {
            'question':
            'Would you rather be able to be free from junk mail or free from email spam for the rest of your life?',
            'id': 187
        },
        {
            'question':
            'Would you rather give up bathing for a month or give up the internet for a month?',
            'id': 188
        },
        {
            'question':
            'Would you rather give up watching TV/movies for a year or give up playing games for a year?',
            'id': 189
        },
        {
            'question':
            'Would you rather never be able to drink sodas like coke again or only be able to drink sodas and nothing else?',
            'id': 190
        },
        {
            'question':
            'Would you rather have amazingly fast typing/texting speed or be able to read ridiculously fast?',
            'id': 191
        },
        {
            'question':
            'Would you rather live under a sky with no stars at night or live under a sky with no clouds during the day?',
            'id': 192
        },
        {
            'question':
            'Would you rather have free Wi-Fi wherever you go or be able to drink unlimited free coffee at any coffee shop?',
            'id': 193
        },
        {
            'question':
            'Would you rather take amazing selfies, but all of your other pictures are horrible or take breathtaking photographs of anything but yourself?',
            'id': 194
        },
        {
            'question':
            'Would you rather never get a paper cut again or never get something stuck in your teeth again?',
            'id': 195
        },
        {
            'question':
            'Would you rather never have another embarrassing fall in public or never feel the need to pass gas in public again?',
            'id': 196
        },
        {
            'question':
            'Would you rather lose your best friend or all of your friends except for your best friend?',
            'id': 197
        },
        {
            'question':
            'Would you rather it never stops snowing (the snow never piles up) or never stops raining (the rain never causes floods)?',
            'id': 198
        },
        {
            'question':
            'Would you rather never be able to leave your own country or never be able to fly in an airplane?',
            'id': 199
        },
        {
            'question':
            'Would you rather never have a toilet clog on you again or never have the power go out again?',
            'id': 200
        },
        {
            'question':
            'Would you rather earbuds and headphones never sit right on / in your ears or have all music either slightly too quiet or slightly too loud?',
            'id': 201
        },
        {
            'question':
            'Would you rather be the best in the world at climbing trees or the best in the world at jumping rope?',
            'id': 202
        },
        {
            'question':
            'Would you rather never run out of battery power for whatever phone and tablet you own or always have free Wi-Fi wherever you go?',
            'id': 203
        },
        {
            'question':
            'Would you rather never have to clean a bathroom again or never have to do dishes again?',
            'id': 204
        },
        {
            'question':
            'Would you rather eat an egg with a half-formed chicken inside or eat ten cooked grasshoppers?',
            'id': 205
        },
        {
            'question':
            'Would you rather only wear one color each day or have to wear seven colors each day?',
            'id': 206
        },
        {
            'question':
            'Would you rather eat rice with every meal and never be able to eat bread or eat bread with every meal and never be able to eat rice?',
            'id': 207
        },
        {
            'question':
            'Would you rather travel the world for a year all expenses paid or have $40,000 to spend on whatever you want?',
            'id': 208
        },
        {
            'question':
            'Would you rather be able to go to any theme park in the world for free for the rest of your life or eat for free at any drive-through restaurant for the rest of your life?',
            'id': 209
        },
        {
            'question':
            'Would you rather be the absolute best at something that no one takes seriously or be well above average but not anywhere near the best at something well respected?',
            'id': 210
        },
        {
            'question':
            'Would you rather it be impossible for you to be woken up for 11 straight hours every day, but you wake up feeling amazing, or you can be woken up normally but never feel totally rested?',
            'id': 211
        },
        {
            'question':
            'Would you rather have everything in your house perfectly organized by a professional or have a professional event company throw the best party you’ve ever been to, in your honor?',
            'id': 212
        },
        {
            'question':
            'Would you rather have unlimited amounts of any material you want to build a house, but you have to build the house all by yourself or have a famed architect design and build you a modest house?',
            'id': 213
        },
        {
            'question':
            'Would you rather never sweat again but not be more prone to heat stroke or never feel cold again but cold still physically affects you (i',
            'id': 214
        },
        {
            'question':
            'Would you rather super sensitive taste or super sensitive hearing?',
            'id': 215
        },
        {
            'question':
            'Would you rather have constantly dry eyes or a constant runny nose?',
            'id': 216
        },
        {
            'question':
            'Would you rather never lose your phone again or never lose your keys again?',
            'id': 217
        },
        {
            'question':
            'Would you rather have out of control body hair or a strong, pungent body odor?',
            'id': 218
        },
        {
            'question':
            'Would you rather be unable to have kids or only be able to conceive quintuplets?',
            'id': 219
        },
        {
            'question':
            'Would you rather clean rest stop toilets or work in a slaughterhouse for a living?',
            'id': 220
        },
        {
            'question':
            'Would you rather lose all your money and valuables or all the pictures you have ever taken?',
            'id': 221
        },
        {
            'question':
            'Would you rather find your true love or a suitcase with five million dollars inside?',
            'id': 222
        },
        {
            'question':
            'Would you rather not be able to see any colors or have mild but constant tinnitus (ringing in the ears)?',
            'id': 223
        },
        {
            'question':
            'Would you rather have chapped lips that never heal or terrible dandruff that can’t be treated?',
            'id': 224
        },
        {
            'question':
            'Would you rather live without hot water for showers/baths or live without a washing machine?',
            'id': 225
        },
        {
            'question':
            'Would you rather be alone for the rest of your life or always be surrounded by annoying people?',
            'id': 226
        },
        {
            'question':
            'Would you rather be locked in a room that is constantly dark for a week or a room that is constantly bright for a week?',
            'id': 227
        },
        {
            'question':
            'Would you rather accidentally be responsible for the death of a child or accidentally be responsible for the deaths of three adults?',
            'id': 228
        },
        {
            'question':
            'Would you rather know when you are going to die or how you are going to die? (You can’t change the time or method of your death',
            'id': 229
        },
        {
            'question':
            'Would you rather have everything you eat be too salty or not salty enough no matter how much salt you add?',
            'id': 230
        },
        {
            'question':
            'Would you rather never have to work again or never have to sleep again (you won’t feel tired or suffer negative health effects)?',
            'id': 231
        },
        {
            'question':
            'Would you rather never use social media sites/apps again or never watch another movie or TV show?',
            'id': 232
        },
        {
            'question':
            'Would you rather be fluent in all languages and never be able to travel or be able to travel anywhere for a year but never be able to learn a word of a different language?',
            'id': 233
        },
        {
            'question':
            'Would you rather be put in a maximum-security federal prison with the hardest of the hardened criminals for one year or be put in a relatively relaxed prison where wall street types are held for ten years?',
            'id': 234
        },
        {
            'question':
            'Would you rather have everything on your phone right now (browsing history, photos, etc',
            'id': 235
        },
        {
            'question':
            'Would you rather be an amazing artist but not be able to see any of the art you created or be an amazing musician but not be able to hear any of the music you create?',
            'id': 236
        },
        {
            'question':
            'Would you rather have everyone laugh at your jokes but not find anyone else’s jokes funny or have no one laugh at your jokes but you still find other people’s jokes funny?',
            'id': 237
        },
        {
            'question':
            'Would you rather wake up in the middle of an unknown desert or wake up in a rowboat on an unknown body of water?',
            'id': 238
        },
        {
            'question':
            'Would you rather always have a great body for your entire life but have slightly below average intelligence or have a mediocre body for your entire life but be slightly above average in intelligence?',
            'id': 239
        },
        {
            'question':
            'Would you rather be in debt for $100,000 or never be able to make more than $3,500 a month?',
            'id': 240
        },
        {
            'question':
            'Would you rather have the police hunting you for a murder you didn’t commit or a psychopathic clown hunting you?',
            'id': 241
        },
        {
            'question':
            'Would you rather be constantly tired no matter how much you sleep or constantly hungry no matter how much you eat?',
            'id': 242
        },
        {
            'question':
            'Would you rather live a comfortable and peaceful life in the woods in a small cabin without much human interaction or a life full of conflict and entertainment in a mansion in a city?',
            'id': 243
        },
        {
            'question':
            'Would you rather walk around work or school for the whole day without realizing there is a giant brown stain on the back of your pants or realize the deadline for that important paper/project was yesterday, and you are nowhere near done?',
            'id': 244
        },
        {
            'question':
            'Would you rather be so afraid of heights that you can’t go to the second floor of a building or be so afraid of the sun that you can only leave the house on rainy days?',
            'id': 245
        },
        {
            'question':
            'Would you rather get tipsy from just one sip of alcohol and ridiculously drunk from just one alcoholic drink or never get drunk no matter how much alcohol you drank?',
            'id': 246
        },
        {
            'question':
            'Would you rather be hired for a well-paying job that you lied to get and have no idea how to do or be about to give the most important presentation of your life but you can’t remember any of the material you prepared?',
            'id': 247
        },
        {
            'question': 'Would you rather be feared by all or loved by all?',
            'id': 248
        },
        {
            'question':
            'Would you rather sell all of your possessions or sell one of your organs?',
            'id': 249
        },
        {
            'question':
            'Would you rather be infamous in history books or be forgotten after your death?',
            'id': 250
        },
        {
            'question':
            'Would you rather be reincarnated as a fly or just cease to exist after you die?',
            'id': 251
        },
        {
            'question':
            'Would you rather never get angry or never be envious?',
            'id': 252
        },
        {
            'question':
            'Would you rather have a horribly corrupt government or no government?',
            'id': 253
        },
        {
            'question':
            'Would you rather be held in high regard by your parents or your friends?',
            'id': 254
        },
        {
            'question':
            'Would you rather be poor but help people or become incredibly rich by hurting people?',
            'id': 255
        },
        {
            'question':
            'Would you rather humans go to the moon again or go to mars?',
            'id': 256
        },
        {
            'question':
            'Would you rather know the uncomfortable truth of the world or believe a comforting lie?',
            'id': 257
        },
        {
            'question':
            'Would you rather die in 20 years with no regrets or die in 50 years with many regrets?',
            'id': 258
        },
        {
            'question':
            'Would you rather be transported permanently 500 years into the future or 500 years into the past?',
            'id': 259
        },
        {
            'question':
            'Would you rather donate your body to science or donate your organs to people who need them?',
            'id': 260
        },
        {
            'question':
            'Would you rather be famous when you are alive and forgotten when you die or unknown when you are alive but famous after you die?',
            'id': 261
        },
        {
            'question':
            'Would you rather go to jail for 4 years for something you didn’t do or get away with something horrible you did but always live in fear of being caught?',
            'id': 262
        },
        {
            'question':
            'Would you rather live in the wilderness far from civilization with no human contact or live on the streets of a city as a homeless person?',
            'id': 263
        },
        {
            'question':
            'Would you rather live your entire life in a virtual reality where all your wishes are granted or just in the normal real world?',
            'id': 264
        },
        {
            'question':
            'Would you rather have a horrible job, but be able to retire comfortably in 10 years or have your dream job, but have to work until the day you die?',
            'id': 265
        },
        {
            'question':
            'Would you rather lose all of your memories from birth to now or lose your ability to make new long-term memories?',
            'id': 266
        },
        {
            'question':
            'Would you rather always be able to see 5 minutes into the future or always be able to see 100 years into the future?',
            'id': 267
        },
        {
            'question':
            'Would you rather be forced to kill one innocent person or five people who committed minor crimes?',
            'id': 268
        },
        {
            'question':
            'Would you rather work very hard at a rewarding job or hardly have to work at a job that isn’t rewarding?',
            'id': 269
        },
        {
            'question':
            'Would you rather have a criminal justice system that actually works and is fair or an administrative branch that is free of corruption?',
            'id': 270
        },
        {
            'question':
            'Would you rather have real political power but be relatively poor or be ridiculously rich and have no political power?',
            'id': 271
        },
        {
            'question':
            'Would you rather have the power to gently nudge anyone’s decisions or have complete puppet master control of five people?',
            'id': 272
        },
        {
            'question':
            'Would you rather live in a utopia as a normal person or in a dystopia but you are the supreme ruler?',
            'id': 273
        },
        {
            'question':
            'Would you rather snitch on your best friend for a crime they committed or go to jail for the crime they committed?',
            'id': 274
        },
        {
            'question':
            'Would you rather be born again in a totally different life or born again with all the knowledge you have now?',
            'id': 275
        },
        {
            'question':
            'Would you rather all conspiracy theories be true or live in a world where no leaders really know what they are doing?',
            'id': 276
        },
        {
            'question':
            'Would you rather know all the mysteries of the universe or know every outcome of every choice you make?',
            'id': 277
        },
        {
            'question':
            'Would you rather spend two years with your soul mate only to have them die and you never love again or spend your life with someone nice you settled for?',
            'id': 278
        },
        {
            'question':
            'Would you rather have all corporations know all of your computer usage or the government know all of your computer usage?',
            'id': 279
        },
        {
            'question':
            'Would you rather inherit 20 million dollars when you turn 18 or spend the time earning 50 million dollars through your hard work?',
            'id': 280
        },
        {
            'question':
            'Would you rather the general public think you are a horrible person, but your family is very proud of you, or your family thinks you are a horrible person, but the general public be very proud of you?',
            'id': 281
        },
        {
            'question':
            'Would you rather fight for a cause you believe in, but doubt will succeed or fight for a cause that you only partially believe in but have a high chance of your cause succeeding?',
            'id': 282
        },
        {
            'question':
            'Would you rather be famous for inventing a deadly new weapon or invent something that helps the world but someone else gets all the credit for inventing it?',
            'id': 283
        },
        {
            'question':
            'Would you rather live in a haunted house where the ghosts ignore you and do their own thing or be a ghost in a house living out a pleasant and uneventful week from your life again and again?',
            'id': 284
        },
        {
            'question':
            'Would you rather write a novel that will be widely considered the most important book in the past 200 years, but you and the book will only be appreciated after your death or be the most famous erotica writer of your generation?',
            'id': 285
        },
        {
            'question':
            'Would you rather have done something horribly embarrassing and only your best friend knows or not done something horribly embarrassing, but everyone except your best friend thinks you did it?',
            'id': 286
        },
        {
            'question':
            'Would you rather your shirts be always two sizes too big or one size too small?',
            'id': 287
        },
        {
            'question':
            'Would you rather find five dollars on the ground or find all your missing socks?',
            'id': 288
        },
        {
            'question':
            'Would you rather have one nipple or two belly buttons?',
            'id': 289
        },
        {
            'question':
            'Would you rather eat a ketchup sandwich or a Siracha sandwich?',
            'id': 290
        },
        {
            'question':
            'Would you rather use a push lawnmower with a bar that is far too high or far too low?',
            'id': 291
        },
        {
            'question':
            'Would you rather eat a box of dry spaghetti noodles or two cups of uncooked rice?',
            'id': 292
        },
        {
            'question':
            'Would you rather eat a spoonful of wasabi or a spoonful of extremely spicy hot sauce?',
            'id': 293
        },
        {
            'question':
            'Would you rather have hands that kept growing as you got older or feet that kept growing as you got older?',
            'id': 294
        },
        {
            'question':
            'Would you rather not be able to open any closed doors (locked or unlocked) or not be able to close any open doors?',
            'id': 295
        },
        {
            'question':
            'Would you rather have plants grow at 20 times their normal rate when you are near or for people and animals to stop aging when you are near them?',
            'id': 296
        },
        {
            'question':
            'Would you rather always feel like someone is following you, but no one is, or always feel like someone is watching you, even though no one is?',
            'id': 297
        },
        {
            'question':
            'Would you rather live in a house with see-through walls in a city or in the same see-through house but in the middle of a forest far from civilization?',
            'id': 298
        },
        {
            'question':
            'Would you rather have every cat or dog that gets lost end up at your house or everyone’s clothes that they forget in the dryer get teleported to your house?',
            'id': 299
        },
        {
            'question':
            'Would you rather blink twice the normal rate or not be able to blink for 5 minutes but then have to close your eyes for 10 seconds every 5 minutes?',
            'id': 300
        },
        {
            'question':
            'Would you rather all plants scream when you cut them / pick their fruit or animals beg for their lives before they are killed?',
            'id': 301
        },
        {
            'question':
            'Would you rather wake up each morning to find that a random animal appendage has replaced your nondominant arm or permanently replace your bottom half with an animal bottom of your choice (not human)?',
            'id': 302
        },
        {
            'question':
            'Would you rather have a map that shows you the location of anything you want to find and can be used again and again but has a margin of error of up to five miles or a device that allows you to find the location of anything you want with incredible accuracy but can only be used three times?',
            'id': 303
        },
        {
            'question':
            'Would you rather have all animals feel compelled to obey you if you come within 10 feet of them or be given the opportunity to genetically design a pet that will be loyal only to you with the combined DNA of three animals?',
            'id': 304
        },
        {
            'question':
            'Would you rather have someone impersonating you and doing really amazing things that you get the credit for or find money hidden in weird places all around your house every day but you can’t figure out where the money comes from or how it keeps getting there?',
            'id': 305
        },
        {
            'question':
            'Would you rather wake up every morning with a new hundred-dollar bill in your pocket but not know where it came from or wake up every morning with a new fifty-dollar bill in your pocket and know where it comes from?',
            'id': 306
        },
        {
            'question':
            'Would you rather have a clown only you can see that follows you everywhere and just stands silently in a corner watching you without doing or saying anything or have a real-life stalker who dresses like the Easter bunny that everyone can see?',
            'id': 307
        },
        {
            'question':
            'Would you rather be an amazing virtuoso at any instrument but only if you play naked or be able to speak any language but only if you close your eyes and dance while you are doing it?',
            'id': 308
        },
        {
            'question':
            'Would you rather everything you dream each night come true when you wake up or everything a randomly chosen person dreams each night come true when they wake up?',
            'id': 309
        },
        {
            'question':
            'Would you rather have a boomerang that would find and kill any one person of your choosing, anywhere in the world, but can only be used once or a boomerang that always returns to you with one dollar?',
            'id': 310
        },
        {
            'question':
            'Would you rather have someone secretly give you LSD on a random day and time once every 6 months or have everyone in the world all take LSD at the same time once every 5 years?',
            'id': 311
        },
        {
            'question':
            'Would you rather all electrical devices mysteriously stop working (possibly forever) or the governments of the world are only run by people going through puberty?',
            'id': 312
        },
    ]
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


@bot.command(aliases=['wiki'])
async def wikipedia_most_viewed(ctx):
    '''
    Get the most visited wikipedia pages yesterday
    '''
    today = datetime.datetime.today() - datetime.timedelta(hours=32)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}"
    headers = {
        'User-Agent': 'Discord Bot/0.1 requests',
    }

    r = requests.get(url, headers=headers)
    articles = r.json()['items'][0]['articles']
    page = ''
    views = ''
    for article in articles[0:12]:
        if article['article'] not in ['Main_Page', 'Special:Search']:
            page += f"{article['article']}\n"
            views += f"{article['views']:,}\n"
    embed = discord.Embed(title='Most Viewed Yesterday')
    embed.add_field(name='Page', value=page, inline=True)
    embed.add_field(name='Views', value=views, inline=True)
    await ctx.send(embed=embed)

keep_alive()
bot.run(TOKEN)
