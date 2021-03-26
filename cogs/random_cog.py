import discord, requests, random
from discord.ext import commands

class RandomCommands(commands.Cog, name='Random Commands'):
    '''Random commands'''

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(aliases=['tsq'])
    async def taylor_swift_quote(self, ctx):
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

    @commands.command(aliases=['ym', 'yomama', 'yomomma'])
    async def yo_mama(self, ctx):
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

    
    @commands.command(aliases=['fortune_cookie'])
    async def advice(self, ctx):
        '''
        Get fortune-cookie-esque advice
        '''
        r = requests.get('https://api.adviceslip.com/advice')
        result = r.json()['slip']['advice']
        await ctx.send(result)


    @commands.command(aliases=['fq'])
    async def friends_quote(self, ctx):
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
        
    @commands.command(aliases=['num', 'num_fact', 'number'])
    async def number_fact(self, ctx, number):
        '''
        Get a fact about a number
        '''
        r = requests.get('http://numbersapi.com/' + number)
        result = r.text
        await ctx.send(result)


    @commands.command(aliases=['bp'])
    async def bread_pun(self, ctx):
        '''
        Get a random bread pun
        '''
        r = requests.get('https://my-bao-server.herokuapp.com/api/breadpuns')
        result = r.text
        await ctx.send(result)
        
    @commands.command(aliases=['chuck', 'norris'])
    async def chuck_norris(self, ctx):
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


    @commands.command(aliases=['kanye'])
    async def kanye_west(self, ctx):
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

    @commands.command()
    async def randrange(self, ctx, low_number, high_number):
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



    @commands.command(aliases=['cook'])
    async def recipe(self, ctx, query, *args):
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


def setup(bot):
	bot.add_cog(RandomCommands(bot))