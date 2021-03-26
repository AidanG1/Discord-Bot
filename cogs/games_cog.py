import discord, requests, datetime
from discord.ext import commands

class GamesCommands(commands.Cog, name='Games Commands'):
    '''Games commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['basketballstocks', 'basketball_stocks'])
    async def bball(self, ctx, player):
        '''
        Get player price on basketballstocks.com using slug
        '''
        url = 'https://www.basketballstocks.com/api/players/' + player
        r = requests.get(url)
        result = r.json()
        await ctx.send(
            f"{result['name']}'s current price is ${result['current_price']}: https://basketballstocks.com/p/{result['slug']} "
        )

    @commands.command(aliases=['nbap'])
    async def nba_player(self, ctx, *args):
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
        current_year = datetime.date.today(
        ).year - 1  # doesn't actually get current nba season
        combined_war_per_82 = result['war_mean_' + str(current_year) + '_BL']
        embed = discord.Embed(
            title=name,
            description=
            f'Team: {team}\n Status: {category}\nLast Year War Per 82: {round(float(combined_war_per_82), 2)}',
            color=discord.Color.purple())
        embed.set_thumbnail(url=url)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['chess'])
    async def chess_stats(self, ctx, username):
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


def setup(bot):
	bot.add_cog(GamesCommands(bot))