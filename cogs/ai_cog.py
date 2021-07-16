import discord, requests, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class AICommands(commands.Cog, name='AI Commands'):
    '''AI commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ai_text_gen', 'ai_text_generation', 'ai'])
    async def text_gen(self, ctx, *, arg):
        '''
        Generate a paragraph from a sentence or phrase using AI
        '''
        message = await ctx.send('loading...')
        r = requests.post("https://api.deepai.org/api/text-generator",
                        data={
                            'text': arg,
                        },
                        headers={'api-key': os.getenv('api-key')})
        await ctx.send(r.json()['output'])
        await message.delete()


    @commands.command(aliases=['sentiment', 'emotion', 'feeling', 'feel'])
    async def sentiment_analysis(self, ctx, *, arg):
        '''
        Sentiment analysis of text
        '''
        message = await ctx.send('loading...')
        r = requests.post("https://api.deepai.org/api/sentiment-analysis",
                        data={
                            'text': arg,
                        },
                        headers={'api-key': os.getenv('api-key')})
        await ctx.send(r.json()['output'])
        await message.delete()


def setup(bot):
	bot.add_cog(AICommands(bot))