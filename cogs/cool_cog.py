import discord, requests, os, random, hashlib, cryptocode
from bs4 import BeautifulSoup
from discord_components import Button
from discord.ext import commands
from dotenv import load_dotenv
from replit import db
from random import randrange
from time import perf_counter
from discord.errors import NotFound

load_dotenv()


class CoolCommands(commands.Cog, name='Cool Commands'):
    '''Cool commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rl'])
    @commands.has_role('Admins')
    async def reload(self, ctx, *, cog):
        '''
        Reloads a cog.
        '''
        extensions = self.bot.extensions
        if cog == 'all':
            for extension in extensions:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            await ctx.send('Done')
        elif cog in extensions:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            await ctx.send('Done')
        else:
            await ctx.send('Unknown Cog')

    @commands.command(aliases=['cb'])
    async def clear_buttons(self, ctx):
        '''
        Clear active buttons
        '''
        self.bot.button_exists = False
        await ctx.send(
            'Buttons have been cleared. Use ^bt or ^button to make a button.')

    @commands.command(aliases=['bt'])
    async def button(self, ctx):
        '''
        Get a button and see who can click fastest
        '''
        rand = randrange(1, 5)
        start_time = perf_counter()
        try:
            button_exists = self.bot.button_exists
        except AttributeError:
            button_exists = False
        if not button_exists:
            m = await ctx.send(rand,
                               components=[[
                                   Button(label="1", style=randrange(1, 4)),
                                   Button(label="2", style=randrange(1, 4)),
                                   Button(label="3", style=randrange(1, 4)),
                                   Button(label="4", style=randrange(1, 4)),
                                   Button(label="5", style=randrange(1, 4)),
                               ]])
            self.bot.button_exists = True

            def check(res):
                self.bot.button_exists = False
                return res.component.label.startswith(str(rand))

            # while True:
            interaction = await self.bot.wait_for("button_click")

            def speed_word(speed):
                if speed < 3:
                    return 'fast!'
                elif speed < 6:
                    return 'could be faster!'
                elif speed < 12:
                    return 'slow'
                else:
                    return '🐢'

            if check(interaction):
                response_time = round(perf_counter() - start_time, 2)
                content = f"Correct for {interaction.user}, :white_check_mark: in {response_time} seconds, {speed_word(response_time)}"
                # await interaction.respond(content = f"Correct, :white_check_mark: in {response_time} seconds, {speed_word(response_time)}")
            else:
                content = f"Incorrect for {interaction.user}, :x:"
            await interaction.respond(content='Answered')
            await m.edit(content,
                         components=[[
                             Button(label="1",
                                    style=randrange(1, 4),
                                    disabled=True),
                             Button(label="2",
                                    style=randrange(1, 4),
                                    disabled=True),
                             Button(label="3",
                                    style=randrange(1, 4),
                                    disabled=True),
                             Button(label="4",
                                    style=randrange(1, 4),
                                    disabled=True),
                             Button(label="5",
                                    style=randrange(1, 4),
                                    disabled=True),
                         ]])
        else:
            await ctx.send('A button already exists')

    @commands.command(aliases=['nyt', 'nytp'])
    async def nyt_popular(self, ctx):
        '''
        Get the real time most popular New York Times article
        '''
        message = await ctx.send('loading...')
        r = requests.get(
            'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key='
            + os.getenv('nyt-key'))
        result = r.json()['results'][0]
        embed = discord.Embed(title=result['title'],
                              url=result['url'],
                              description=result['abstract'],
                              color=discord.Color.green())
        embed.set_image(url=result['media'][0]['media-metadata'][2]['url'])
        await ctx.send(embed=embed)
        await message.delete()

    @commands.command(aliases=['apod', 'space', 'space_picture'])
    async def astronomy_picture(self, ctx):
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

    @commands.command(aliases=['disc'])
    async def disclaimer(self, ctx, *, arg='A'):
        '''
        Send a disclaimer about PAA after a message
        '''
        message = await ctx.reply(
            f'Disclaimer from <@!{ctx.message.author.id}>: **The advice in the replied message should not supersede what a PAA says**'
        )

    @commands.command(aliases=['cwc'])
    async def channel_word_count(self, ctx, word='a', limit=100):
        '''
        Count usages of word in a channel
        '''
        timer = perf_counter()
        loading_message = await ctx.send('loading...')
        channel_history = await ctx.channel.history(limit=limit).flatten()
        count_dict = {}
        for message in channel_history:
            word_count = message.content.lower().count(word)
            if word_count > 0:
                author = message.author.display_name.replace(
                    '||', '| |').replace('**', '* *').replace('__', '_ _')
                if author in count_dict:
                    count_dict[author] += word_count
                else:
                    count_dict[author] = word_count
        count_list = sorted(list(count_dict.items()),
                            key=lambda x: x[1],
                            reverse=True)[0:10]
        user = ''
        counts = ''
        for value in count_list:
            user += f"{value[0]}\n"
            counts += f"{value[1]}\n"
        if len(user) + len(counts) > 1024:
            await ctx.send(
                'Message too long. Decrease the count for the message to send.'
            )
        else:
            embed = discord.Embed(
                title=
                f'"{word.title()}" Count over {limit} most recent messages on #{ctx.channel.name}',
                color=discord.Color.gold())
            embed.add_field(name='User', value=user, inline=True)
            embed.add_field(name=f'{word.title()} Count',
                            value=counts,
                            inline=True)
            await ctx.send(embed=embed)
        await loading_message.delete()
        total_time = perf_counter() - timer
        await ctx.send(
            f'Execution time: {round(total_time,2)} seconds. Iterated through {round(limit/total_time,4)} messages per second.'
        )

    @commands.command(aliases=['cxkcd', 'rxkcd'])
    async def recent_xkcd(self, ctx):
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

    @commands.command(aliases=['xkcd'])
    async def random_xkcd(self, ctx):
        '''
        Get a random xkcd
        '''
        r = requests.get('https://xkcd.com/info.0.json')
        rand_num = random.randrange(1, r.json()['num'])
        r = requests.get(f'https://xkcd.com/{rand_num}/info.0.json')
        result = r.json()
        embed = discord.Embed(
            title=f"{result['title']}: https://xkcd.com/{result['num']}",
            description=result['alt'],
            color=discord.Color.dark_teal())
        embed.set_image(url=result['img'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CoolCommands(bot))
