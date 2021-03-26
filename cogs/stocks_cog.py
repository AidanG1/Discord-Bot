import discord, requests, random
from discord.ext import commands
from cogs.ticker_list import tickers

class StockCommands(commands.Cog, name='Stock Commands'):
    '''Stock commands'''

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(aliases=['sg'])
    async def stock_guess(self, ctx, indic_type):
        '''
        The bot picks a random stock and you guess the value of 1yr change,market cap, pe, or forward pe
        '''
        if indic_type.lower() in ['cap', 'mcap', 'market_cap', 'mktcap']:
            cnbc_type = 'mktcap'
        elif indic_type.lower() in [
                'yragopricechangepct', 'pctch', 'changepct', '1yr', '1yrchange',
                '1y'
        ]:
            cnbc_type = 'yragopricechangepct'
        elif indic_type.lower() in ['fpe', 'forwardpe', 'forward_pe']:
            cnbc_type = 'fpe'
        elif indic_type.lower() in ['pe', 'price_earnings']:
            cnbc_type = 'pe'
        ticker = random.choice(tickers)
        r = requests.get(
            'https://quote.cnbc.com/quote-html-webservice/quote.htm?output=json&requestMethod=quick&symbols='
            + ticker)
        company_name = r.json()['QuickQuoteResult']['QuickQuote']['onAirName']
        value = float(r.json()['QuickQuoteResult']['QuickQuote']['FundamentalData']
                    [cnbc_type])
        value_range = []
        value_range.append(value * 0.94)
        value_range.append(value)
        value_range.append(value * 1.06)
        self.bot.value_range = value_range
        self.bot.value = value
        self.bot.company_name = company_name
        self.bot.indic_type = indic_type
        self.bot.stock_guesses = []
        self.bot.ticker = ticker
        await ctx.send(
            f'Guess the current {indic_type} of {company_name} ({ticker}) (type ^g and then the value to guess)'
        )


    @commands.command(aliases=['g'])
    async def guess(self, ctx, value):
        '''
        Answer a stock question
        '''
        message = f'The value of {self.bot.indic_type} for {self.bot.company_name} ({self.bot.ticker}) is {self.bot.value}'
        if value in ['igu', 'i_give_up']:
            await ctx.send('Answer: ' + message)
            return
        guess = float(value)
        self.bot.stock_guesses.append(guess)
        if guess > self.bot.value_range[0] and guess < self.bot.value_range[2]:
            await ctx.send('Correct! ' + message)
        else:
            pct_off = abs(100 * (guess - self.bot.value) / self.bot.value)
            if pct_off > 100:
                closeness = 'extremely far.'
            elif pct_off > 75:
                closeness = 'very far.'
            elif pct_off > 50:
                closeness = 'far.'
            elif pct_off > 50:
                closeness = 'far.'
            elif pct_off > 25:
                closeness = 'somewhat close.'
            elif pct_off > 15:
                closeness = 'close.'
            elif pct_off > 10:
                closeness = 'very close.'
            elif pct_off > 6:
                closeness = 'extremely close.'
            await ctx.send('Incorrect. You are ' + closeness)
        
    @commands.command()
    async def stock_outlook(self, ctx, stock):
        '''
        Get an outlook for a stock. The outlook is randomly selected
        '''
        phrases = [
            f'{stock} looks very overpriced',
            f'{stock} is a great value right now',
            f'{stock} to the moon',
            f'There are bulls, there are bears, and then there are absolute failures which is what you are if you buy {stock}',
            f'{stock} is not stonks',
            f'{stock} is the next GameStop',
            f"Can't stop won't stop {stock}stock",
            f"I can't wait to lose all of my money on {stock}",
            f"Puts on {stock}",
            f"I wouldn't want {stock} if you paid me for it",
            f"I would rather buy puts on {stock} than put food on my table",
            f"If I didn't lose all my money on SHLD and BBI I would buy {stock}",
        ]
        await ctx.send('This is not financial advice: ' + random.choice(phrases))


def setup(bot):
	bot.add_cog(StockCommands(bot))