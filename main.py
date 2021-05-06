import discord, os, random, requests, asyncio, datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
from keep_alive import keep_alive
from replit import db

load_dotenv()

help_command = commands.DefaultHelpCommand(no_category='General Commands')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='^',
                   help_command=help_command,
                   intents=intents)

TOKEN = os.getenv('TOKEN')

extensions = [
    'cogs.ai_cog',
    'cogs.cool_cog',
    'cogs.games_cog',
    'cogs.ping_yin_cog',
    'cogs.random_cog',
    'cogs.stocks_cog',
    'cogs.wiki_cog',
    'cogs.wyr_cog',
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="^help"))
    countdown_till_o_week.start()


@tasks.loop(hours=24)
async def countdown_till_o_week():
    message_channel = bot.get_channel(787069147359608848)
    o_week_date = datetime.date(2021, 8, 15)
    current_date = datetime.date.today()
    delta = o_week_date - current_date
    print(f'{abs(delta.days)} days until OwOweek!')
    message = await message_channel.send(
        f'{abs(delta.days)} days until OwOweek!')
    await message.add_reaction('1️:partying_face:')
    pce_channel = bot.get_channel(787069147359608848)
    # await pce_channel.invoke(bot.get_command('wikipedia_most_viewed'))


@countdown_till_o_week.before_loop
async def before_countdown_till_o_week():
    for _ in range(60 * 60 * 24):  # loop the whole day
        dt_full = datetime.datetime.now()
        print(dt_full)
        if dt_full.hour == 14 and dt_full.minute == 00:  # 24 hour format
            print('correct time')
            return
        await asyncio.sleep(30)


@bot.event
async def on_message(message):
    if message.content.lower().replace(' ', '').replace('*', '').replace(
            '_', '').replace('|','') == 'poggers':
        if message.author != bot.user:
            await message.channel.send(message.content)
            if len(db.prefix('poggers')) > 0:
                db['poggers'] += 1
            else:
                db['poggers'] = 1
    if '$$$' in message.content:
        loading_message = await message.channel.send('loading...')
        split_message = message.content.replace('\n',' ').split('$$$')[1:]
        tickers = []
        for split_mess in split_message:
            tickers.append(split_mess.split(' ')[0])
        ticker_messages = []
        sending_message_boolean = False
        current_time = (datetime.datetime.now() - datetime.timedelta(hours=5)).time()
        pre_market = False
        post_market = False
        if current_time <= datetime.time(9, 30):
            pre_market = True
        if current_time >= datetime.time(16):
            post_market = True
        for ticker in tickers:
            if len(ticker) == 0:
                continue
            characters_to_remove = [',', ';', '-', '?', '!', '.']
            while True:
                if ticker[-1] in characters_to_remove:
                    ticker = ticker[:-1]
                else:
                    break
            api_link = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&crumb=BriRho6N.D9&lang=en-US&region=US&modules=price%2CsummaryDetail&corsDomain=finance.yahoo.com'
            r = requests.get(api_link).json()['quoteSummary']
            if type(r['result']) == type(None):
                await message.channel.send(r['error']['description'])
            else:  
                sending_message_boolean = True  
                r=r['result'][0]
                current_price = r['price']['regularMarketPrice']['fmt']
                change_percent = r['price']['regularMarketChangePercent']['fmt']
                if r['price']['regularMarketChangePercent']['raw'] < 0:
                    up_down = 'down'
                else:
                    up_down = 'up'
                if len(r['summaryDetail']['marketCap']) == 0:
                    market_cap = 'N/A'
                else:
                    market_cap = r['summaryDetail']['marketCap']['fmt']
                fifty_day_sma = r['summaryDetail']['fiftyDayAverage']['fmt']
                two_hundred_day_sma = r['summaryDetail']['twoHundredDayAverage'][
                    'fmt']
                fifty_two_week_low = r['summaryDetail']['fiftyTwoWeekLow']['fmt']
                fifty_two_week_high = r['summaryDetail']['fiftyTwoWeekHigh']['fmt']
                company_name = r['price']['longName']
                current_message = f'{company_name} (**{ticker.upper()}**) is currently **${current_price}** and is {up_down} **{change_percent}** today. Their market cap is **${market_cap}**, 50 day SMA: ${fifty_day_sma}, 200 day SMA: ${two_hundred_day_sma}, 52 week low: ${fifty_two_week_low}, 52 week high: ${fifty_two_week_high}.'
                if r['price']['quoteType'] == 'EQUITY':
                    if pre_market:
                        pre_market_change = r['price']['preMarketChangePercent']['fmt']
                        current_message += f' Their premarket change is **{pre_market_change}**.'
                    elif post_market:
                        post_market_change = r['price']['postMarketChangePercent']['fmt']
                        current_message += f' Their after market change is **{post_market_change}**.'
                ticker_messages.append(
                    current_message
                )
            if len(db.prefix('three_dollar_stock')) > 0:
                db['three_dollar_stock'] += 1
            else:
                db['three_dollar_stock'] = 1
        if sending_message_boolean:
            current_message = 0
            messages_to_send = ['']
            for ticker_message in ticker_messages:
                if len(messages_to_send[current_message]) == 0:
                    messages_to_send[current_message] = ticker_message
                elif len(ticker_message) + len(
                        messages_to_send[current_message]) >= 2000:
                    messages_to_send.append(ticker_message)
                    current_message += 1
                else:
                    messages_to_send[current_message] += '\n'
                    messages_to_send[current_message] += ticker_message
            for message_to_send in messages_to_send:
                await message.channel.send(message_to_send)
        await loading_message.delete()

    bruh_count = message.content.lower().count('bruh')
    if bruh_count > 0:
        author = message.author
        if author != bot.user:
            db_name = 'bruh_' + str(author).replace('#', '')
            if len(db.prefix(db_name)) > 0:
                db[db_name] += bruh_count
            else:
                db[db_name] = bruh_count
            if db['bruh_counter_enabled'] == True:
                await message.channel.send(
                    f'Bruh counter for {author} is now {db[db_name]}')
    await bot.process_commands(message)


@bot.event
async def on_command(ctx):
    if len(db.prefix(ctx.command)) > 0:
        db[ctx.command] += 1
    else:
        db[ctx.command] = 1


@bot.command(aliases=['cfrq', 'frq'])
async def command_frequency(ctx, count='10'):
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
    for key in key_list[0:int(count)]:
        command += f"{key[0]}\n"
        times_run += f"{key[1]}\n"
    if len(command) + len(times_run) > 1024:
        await ctx.send(
            'Message too long. Decrease the count for the message to send.')
    else:
        embed = discord.Embed(title='Most Run Commands',
                              color=discord.Color.gold())
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
        db['bruh_counter_enabled'] = not db['bruh_counter_enabled']
        await ctx.send(f"The bruh counter is now {db['bruh_counter_enabled']}")


@bot.command(aliases=['bc'])
async def bruhCount(ctx, count='10'):
    '''
    Get bruh count
    '''
    message = await ctx.send('loading...')
    keys = db.keys()
    filtered_keys = [key for key in keys if key[0:5] == 'bruh_']
    bruh_keys = []
    for i in range(len(filtered_keys)):
        if '#' not in filtered_keys[i]:
            bruh_keys.append([filtered_keys[i], db[filtered_keys[i]]])
            bruh_keys = sorted(bruh_keys, key=lambda x: x[1],
                               reverse=True)[0:int(count)]
    user = ''
    bruhs = ''
    for key in bruh_keys:
        user += f"{key[0][5:]}\n"
        bruhs += f"{key[1]}\n"
    if len(user) + len(bruhs) > 1024:
        await ctx.send(
            'Message too long. Decrease the count for the message to send.')
    else:
        embed = discord.Embed(title='User Bruh Count',
                              color=discord.Color.gold())
        embed.add_field(name='User', value=user, inline=True)
        embed.add_field(name='Bruh Count', value=bruhs, inline=True)
        await ctx.send(embed=embed)
    await message.delete()


@bot.command(aliases=['mbc'])
async def myBruhCount(ctx):
    '''
    Get your personal bruh count
    '''
    message = await ctx.send('loading...')
    db_key = 'bruh_' + str(ctx.message.author).replace('#', '')
    value = db[db_key]
    await ctx.send(f'The bruh count for {ctx.message.author} is {value}.')
    await message.delete()


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


@bot.command(aliases=['rm'])
async def role_members(ctx, role: discord.Role):
    '''
    Get the number of members in a role by @tting the role
    '''
    await ctx.send(f'The role {role.name} has {len(role.members)} members')


@bot.command(aliases=['rmm'])
async def role_members_multiple(ctx, role1: discord.Role, role2: discord.Role):
    '''
    Get the number who share 2 roles by @tting both of them
    '''
    role1_members = [member.name for member in role1.members]
    role2_members = [member.name for member in role2.members]
    await ctx.send(
        f'The roles {role1.name} and {role2.name} have {len(set(role1_members) & set(role2_members))} members in common'
    )


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send("That command does not exist. Use ^help to get a list of commands.")

keep_alive()
bot.run(TOKEN)
