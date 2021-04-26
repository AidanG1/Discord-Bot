import discord, requests, os, random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class CoolCommands(commands.Cog, name='Cool Commands'):
    '''Cool commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nyt', 'nytp'])
    async def nyt_popular(self, ctx):
        '''
        Get the real time most popular New York Times article
        '''
        message = await ctx.send('loading...')
        r = requests.get(
            'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=' +
            os.getenv('nyt-key'))
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