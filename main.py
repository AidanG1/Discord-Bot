import discord, os, random, requests, asyncio, datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
from keep_alive import keep_alive
from replit import db
from discord_components import DiscordComponents

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
    'cogs.anon_cog',
    'cogs.cool_cog',
    'cogs.games_cog',
    'cogs.lyrics_cog',
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
    DiscordComponents(bot)
    print(f'Bot connected as {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="^help"))
    # countdown_till_o_week.start()
    docstring_reminder.start()


# @tasks.loop(hours=24)
# async def countdown_till_o_week():
#     message_channel = bot.get_channel(787069147359608848)
#     o_week_date = datetime.date(2022, 4, 9)
#     current_date = datetime.date.today()
#     delta = o_week_date - current_date
#     print(f'{abs(delta.days)} days until Beer Bike!')
#     message = await message_channel.send(
#         f'{abs(delta.days)} days until Beer Bike!')
#     await message.add_reaction('1️:partying_face:')
# @countdown_till_o_week.before_loop
# async def before_countdown_till_o_week():
#     for _ in range(60 * 60 * 24):  # loop the whole day
#         dt_full = datetime.datetime.now()
#         print(dt_full)
#         if dt_full.hour == 14 and dt_full.minute == 00:  # 24 hour format
#             print('correct time')
#             return
#         await asyncio.sleep(30)
@tasks.loop(hours=24)
async def docstring_reminder():
    message_channel = bot.get_channel(880187153223675945)
    await message_channel.send(
        f"Don't forget about docstrings! ||docstrings may or may not be present in the code for this bot||")

@docstring_reminder.before_loop
async def before_docstring_reminder():
    for _ in range(60 * 60 * 24):  # loop the whole day
        dt_full = datetime.datetime.now()
        print(dt_full)
        if dt_full.hour == 21 and dt_full.minute == 32:  # 24 hour format
            print('correct time')
            return
        await asyncio.sleep(30)

@bot.event
async def on_message(message):
    if message.content.lower().replace(' ', '').replace('*', '').replace('~','').replace(
            '_', '').replace('|','') == 'poggers':
        if message.author != bot.user:
            await message.reply(message.content)
            if len(db.prefix('frq_poggers')) > 0:
                db['frq_poggers'] += 1
            else:
                db['frq_poggers'] = 1
    words_to_count = ('bruh', 'indeed', 'pog')
    for word in words_to_count:
        word_count = message.content.lower().count(word)
        if word_count > 0:
            author = message.author
            if author != bot.user:
                db_name = word + '_' + str(author).replace('#', '')
                if len(db.prefix(db_name)) > 0:
                    db[db_name] += word_count
                else:
                    db[db_name] = word_count
                if db['word_counter_enabled']:
                    await message.channel.send(
                        f'{word.title()} counter for {author} is now {db[db_name]}')
    # doesn't check if message sender is bot so will keep sending forever
    # if 'koyfin' in message.content.lower() and message.channel.id == 804216164284629032:
    #     await message.channel.send("Koyfin's update adding paid plans came at the expense of the free plan and forced users to pay basically 1000 dollars a year for a usable product, ruining the product.")
    if '$$' in message.content:
        loading_message = await message.channel.send('loading...')
        split_message = message.content.replace('\n',' ').split('$$')[1:]
        tickers = []
        for split_mess in split_message:
            tickers.append(split_mess.split(' ')[0])
        ticker_messages = []
        sending_message_boolean = False
        for ticker in tickers:
            if len(ticker) == 0:
                continue
            characters_to_remove = [',', ';', '-', '?', '!', '.', '*', '|', '(', ')', '[', ']', '{', '}', "'", '"']
            while True:
                if ticker[-1] in characters_to_remove: #only want to remove from the end because some tickers have punctuation in them
                    ticker = ticker[:-1]
                else:
                    break
            if '$' in ticker:
                split_ticker = ticker.split('$')
                ticker = split_ticker[0]
                graph_settings = split_ticker[1]
                # numbers: 1: 10 day, 2: 2 day, 3: 5 day, 4: 1 month, 5: 2 month, 6: 3 month, 7: 6 month, 19: YTD, 8: 1 year, 9 : 2 year, 10: 3 year, 11: 4 year, 12: 5 year, 13: decade, 20: all time
                frequency = 1
                if len(graph_settings) != 0 and int(graph_settings) <= 3:
                    frequency = 6
                await message.channel.send(f'https://api.wsj.net/api/kaavio/charts/big.chart?nosettings=1&symb={ticker}&uf=0&type=4&size=2&style=350&freq={frequency}&entitlementtoken=0c33378313484ba9b46b8e24ded87dd6&time={graph_settings}&rand=1111111&compidx=aaaaa%3a0&ma=3&maval=50&lf=2&lf2=4&lf3=0&height=444&width=579&mocktick=1')
            api_link = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?formatted=true&crumb=BriRho6N.D9&lang=en-US&region=US&modules=price%2CsummaryDetail&corsDomain=finance.yahoo.com'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            r = requests.get(api_link, headers=headers)
            r = r.json()['quoteSummary']
            if type(r['result']) == type(None):
                await message.channel.send(r['error']['description'])
            else:  
                sending_message_boolean = True  
                r=r['result'][0]
                try:
                    if len(r['price']['regularMarketPrice']) == 0:
                        current_price = 0
                    else:
                        current_price = r['price']['regularMarketPrice']['fmt']
                    if len(r['price']['regularMarketChangePercent']) == 0:
                        change_percent = 0
                    else:
                        change_percent = r['price']['regularMarketChangePercent']['fmt']
                    if r['price']['regularMarketChangePercent']['raw'] < 0:
                        up_down = 'down'
                    else:
                        up_down = 'up'
                    if 'summaryDetail' in r:
                        if len(r['summaryDetail']['marketCap']) == 0:
                            market_cap = 'N/A'
                        else:
                            market_cap = r['summaryDetail']['marketCap']['fmt']
                        if len(r['summaryDetail']['fiftyDayAverage']) == 0:
                            fifty_day_sma = 'N/A'
                        else:
                            fifty_day_sma = r['summaryDetail']['fiftyDayAverage']['fmt']
                        if len(r['summaryDetail']['twoHundredDayAverage']) == 0:
                            two_hundred_day_sma = 'N/A'
                        else:
                            two_hundred_day_sma = r['summaryDetail']['twoHundredDayAverage']['fmt']
                        fifty_two_week_low = r['summaryDetail']['fiftyTwoWeekLow']['fmt']
                        fifty_two_week_high = r['summaryDetail']['fiftyTwoWeekHigh']['fmt']
                    else:
                        market_cap = 'N/A'
                        fifty_day_sma = 'N/A'
                        two_hundred_day_sma = 'N/A'
                        fifty_two_week_low = 'N/A'
                        fifty_two_week_high = 'N/A'
                    company_name = r['price']['longName']
                    current_message = f'{company_name} (**{ticker.upper()}**) is currently **${current_price}** and is {up_down} **{change_percent}** today. Their market cap is **${market_cap}**, 50 day SMA: ${fifty_day_sma}, 200 day SMA: ${two_hundred_day_sma}, 52 week low: ${fifty_two_week_low}, 52 week high: ${fifty_two_week_high}.'
                    try:
                        if r['price']['quoteType'] == 'EQUITY':
                            if r['price']['marketState'] == 'PRE':
                                pre_market_change = r['price']['preMarketChangePercent']['fmt']
                                current_message += f" Their premarket change is **{pre_market_change}** and the price is **${r['price']['preMarketPrice']['fmt']}**."
                            elif 'POST' in r['price']['marketState'] or r['price']['marketState'] == 'PREPRE':
                                post_market_change = r['price']['postMarketChangePercent']['fmt']
                                current_message += f" Their after market change is **{post_market_change}** and the price is **${r['price']['postMarketPrice']['fmt']}**."
                    except KeyError:
                        pass
                    ticker_messages.append(
                        current_message
                    )
                except KeyError:
                    await message.channel.send(f'Error fetching info for {ticker}')
                
            if len(db.prefix('frq_two_dollar_stock')) > 0:
                db['frq_two_dollar_stock'] += 1
            else:
                db['frq_two_dollar_stock'] = 1
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
    
    await bot.process_commands(message)


@bot.event
async def on_command(ctx):
    if len(db.prefix('frq_' + str(ctx.command))) > 0:
        db['frq_' + str(ctx.command)] += 1
    else:
        db['frq_' + str(ctx.command)] = 1


@bot.command(aliases=['cfrq', 'frq'])
async def command_frequency(ctx, count='10'):
    '''
    Get the amount of times that each command has been run
    '''
    keys = db.prefix('frq_')
    key_list = []
    for key in keys:
        if '#' not in key and not key[-1].isdigit():
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


@bot.command(aliases=['cp'])
@commands.has_role('Admins')
async def change_presence(ctx, type, *, arg):
    '''
    Admin only command to change bot presence
    '''
    phrase = arg.title()
    if type[0].lower() == 'l':
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name=phrase))
    elif type[0].lower() in ['g', 'p']:
        await bot.change_presence(activity=discord.Game(name=phrase))
    else:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=phrase))


@bot.command(aliases=['ce', 'wce'])
# @commands.has_role('Admins')
async def wordCounter_enabled(ctx):
    '''
    Admin only command to change whether the bruh counter is enabled
    '''
    if len(db.prefix('word_counter_enabled')) == 0:
        db['word_counter_enabled'] = True
    else:
        db['word_counter_enabled'] = not db['word_counter_enabled']
        await ctx.send(f"The word counter is now {db['word_counter_enabled']}")


@bot.command(aliases=['wc'])
async def wordCount(ctx, word='bruh', count='10'):
    '''
    Get word count
    '''
    message = await ctx.send('loading...')
    word = word.lower()
    keys = db.keys()
    filtered_keys = [key for key in keys if key[0:(len(word) + 1)] == word + '_']
    if len(filtered_keys) == 0:
        await message.delete()
        await ctx.send(word + ' not in database')
    else:
        db_keys = []
        for i in range(len(filtered_keys)):
            if '#' not in filtered_keys[i]:
                db_keys.append([filtered_keys[i], db[filtered_keys[i]]])
                db_keys = sorted(db_keys, key=lambda x: x[1],
                                reverse=True)[0:int(count)]
        user = ''
        words = ''
        for key in db_keys:
            user += f"{key[0][(len(word) + 1):-4]}\n"
            words += f"{key[1]}\n"
        if len(user) + len(words) > 1024:
            await ctx.send(
                'Message too long. Decrease the count for the message to send.')
        else:
            embed = discord.Embed(title=f'User {word.title()} Count',
                                color=discord.Color.gold())
            embed.add_field(name='User', value=user, inline=True)
            embed.add_field(name=f'{word.title()} Count', value=words, inline=True)
            await ctx.send(embed=embed)
        await message.delete()


@bot.command(aliases=['ubc', 'uwc'])
async def userWordCount(ctx, user):
    '''
    Get a user's word count
    '''
    message = await ctx.send('loading...')
    for character in ['<', '@', '!', '>']:
        user = user.replace(character, '')
    user= await bot.fetch_user(user)
    keys = []
    for key in db.keys():
        if key.split('_', 1)[-1] == str(user).replace('#', ''):
            keys.append(key)
    word_message = ''
    for db_key in keys:
        try:
            value = db[db_key]
        except KeyError:
            value = 0
        word_message += f'The {db_key.split("_")[0]} count for {user} is {value}. \n'
    await ctx.send(word_message)
    await message.delete()
    


@bot.command(aliases=['code'])
async def get_code(ctx):
    '''
    Get the code for this bot
    '''
    await ctx.send('https://repl.it/@AidanGerber/Discord-Bot#main.py\nhttps://github.com/AidanG1/Discord-Bot')


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
