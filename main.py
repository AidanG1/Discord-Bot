import discord, os, random, requests, asyncio, datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
from keep_alive import keep_alive
from replit import db

load_dotenv()

help_command = commands.DefaultHelpCommand(no_category='General Commands')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='^', help_command=help_command, intents=intents)

TOKEN = os.getenv('TOKEN')

extensions = [
	'cogs.ai_cog',
    'cogs.cool_cog',
    'cogs.games_cog',
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


@tasks.loop(hours = 24)
async def countdown_till_o_week():
    message_channel = bot.get_channel(787069147359608848)
    o_week_date = datetime.date(2021, 8, 15)
    current_date = datetime.date.today()
    delta = o_week_date - current_date
    print(f'{abs(delta.days)} days until OwOweek!')
    message = await message_channel.send(f'{abs(delta.days)} days until OwOweek!')
    await message.add_reaction('1️:partying_face:')
    pce_channel = bot.get_channel(787069147359608848)
    # await pce_channel.invoke(bot.get_command('wikipedia_most_viewed'))


@countdown_till_o_week.before_loop
async def before_countdown_till_o_week():
    for _ in range(60*60*24):  # loop the whole day
        dt_full = datetime.datetime.now()
        print(dt_full)
        if dt_full.hour == 14 and dt_full.minute == 00:  # 24 hour format
            print('correct time')
            return
        await asyncio.sleep(30)

@bot.event
async def on_message(message):
    if message.content == 'test Rice bot':
        await message.channel.send('Testing 1 2 3!')
    if message.content.lower().replace(' ', '').replace('*', '') .replace('_', '') == 'poggers':
        if message.author != bot.user:
            await message.channel.send(message.content)
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
    await ctx.send(f'The roles {role1.name} and {role2.name} have {len(set(role1_members) & set(role2_members))} members in common')

@bot.command(aliases=['bc'])
async def bruhCount(ctx):
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
                               reverse=True)[0:10]
    user = ''
    bruhs = ''
    for key in bruh_keys:
        user += f"{key[0][5:]}\n"
        bruhs += f"{key[1]}\n"
    embed = discord.Embed(title='User Bruh Count', color=discord.Color.gold())
    embed.add_field(name='User', value=user, inline=True)
    embed.add_field(name='Bruh Count', value=bruhs, inline=True)
    await ctx.send(embed=embed)
    await message.delete()


@bot.command(aliases=['get_ping'])
async def ping(ctx):
    '''
    Get bot ping
    '''
    channel_id = discord.utils.get(ctx.guild.channels, name='general').id
    print(channel_id)
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

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send("That command does not exist. Use ^help to get a list of commands.")

keep_alive()
bot.run(TOKEN)
