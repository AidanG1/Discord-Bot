import discord, requests, datetime
from discord.ext import commands


class PingYinCommands(commands.Cog, name='Ping Yin Commands'):
    '''Ping Yin commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yang(self, ctx):
        '''
        yin
        '''
        await ctx.send('yin')

    @commands.command()
    async def yin(self, ctx):
        '''
        yang
        '''
        await ctx.send('yang')

    @commands.command()
    async def pong(self, ctx):
        '''
        ping
        '''
        await ctx.send('ping')

    @commands.command(aliases=['get_ping'])
    async def ping(self, ctx):
        '''
        Get bot ping
        '''
        channel_id = discord.utils.get(ctx.guild.channels, name='general').id
        print(channel_id)
        latency = self.bot.latency
        await ctx.send(f'Latency: {round(latency, 4)} seconds')


def setup(bot):
    bot.add_cog(PingYinCommands(bot))
