import discord, requests, random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
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
                'yragopricechangepct', 'pctch', 'changepct', '1yr',
                '1yrchange', '1y'
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
        value = float(r.json()['QuickQuoteResult']['QuickQuote']
                      ['FundamentalData'][cnbc_type])
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

    @commands.command(aliases=['so'])
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
        await ctx.send('This is not financial advice: ' +
                       random.choice(phrases))

    @commands.command(aliases=['yft'])
    async def yahoo_finance_trending(self, ctx, count='10'):
        '''
        Get Yahoo Finance Trending stocks list
        '''
        message = await ctx.send('loading...')
        r = requests.get(
            f'https://query2.finance.yahoo.com/v1/finance/trending/US?count={count}'
        ).json()['finance']['result'][0]['quotes']
        quotes = [quote['symbol'] for quote in r]
        yft_message = f'Top {count} trending items on Yahoo Finance: ' + ', '.join(
            quotes)[:-2]
        if len(yft_message) > 2000:
            yft_message = 'Message is too long. Please decrease count and try again.'
        await ctx.send(yft_message)
        await message.delete()
    
    @commands.command(aliases=['sad'])
    async def seeking_alpha_description(self, ctx, ticker):
        '''
        Get the seeking alpha summary of a company by ticker
        '''
        message = await ctx.send('loading...')
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.chrome),
            'referrer':
            f'https://seekingalpha.com/symbol/{ticker}?source%3Dcontent_type%253Areact%257Csource%253Asearch-basic',
            'sec-ch-ua':
            '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'accept-language':
            'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6'
        }
        r = requests.get(
            f'https://seekingalpha.com/api/v3/symbol_data?fields[]=long_desc&slugs={ticker}',
            headers=headers).json()
        await ctx.send(r['data'][0]['attributes']['longDesc'])
        await message.delete()
    
    @commands.command(aliases=['cnbcd'])
    async def cnbc_description(self, ctx, ticker):
        '''
        Get the cnbc description of a company by ticker
        '''
        message = await ctx.send('loading...')
        r = requests.get('https://www.cnbc.com/quotes/' + ticker + '?tab=profile').text
        soup = BeautifulSoup(r, 'html.parser')
        try:
            profile = soup.find(class_='CompanyProfile-summary').div.span.text
            await ctx.send(profile)
        except AttributeError:
            await ctx.send(f'CNBC does not have a description for {ticker}')
        await message.delete()

    @commands.command(aliases=['wsjd', 'd'])
    async def wsj_description(self, ctx, ticker):
        '''
        Get the WSJ description of a company by ticker
        '''
        message = await ctx.send('loading...')
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.chrome)
        }
        r = requests.get(f'https://www.wsj.com/market-data/quotes/{ticker}/company-people', headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        try:
            profile = soup.find(class_='txtBody').text
            await ctx.send(profile)
        except AttributeError:
            await ctx.send(f'WSJ does not have a description for {ticker}')
        await message.delete()

    @commands.command(aliases=['tsd'])
    async def the_street_description(self, ctx, ticker):
        '''
        Get the Street description of a company by ticker
        '''
        message = await ctx.send('loading...')
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.chrome)
        }
        try:
            r = requests.get(f'https://api.thestreet.com/marketdata/2/1?includePartnerContent=true&includeLatestNews=false&start=0&rt=true&max=10&filterContent=false&format=json&s={ticker}&includePartnerNews=false', headers=headers).json()['response']['quotes'][0]['description']
            await ctx.send(r)
        except AttributeError:
            await ctx.send(f'The Street does not have a description for {ticker}')
        await message.delete()

    @commands.command(aliases=['msnd'])
    async def msn_description(self, ctx, ticker):
        '''
        Get the MSN description of a company by ticker
        '''
        message = await ctx.send('loading...')
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.chrome)
        }
        r = requests.get(f'https://www.msn.com/en-us/money/stockdetails/company?symbol={ticker}', headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        try:
            profile = soup.find(class_='company-description').text
            await ctx.send(profile)
        except AttributeError:
            await ctx.send(f'MSN does not have a description for {ticker}')
        await message.delete()

    @commands.command(aliases=['investd'])
    async def investopedia_description(self, ctx, ticker):
        '''
        Get the Investopedia description of a company by ticker
        '''
        message = await ctx.send('loading...')
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.chrome)
        }
        r = requests.get(f'https://www.investopedia.com/markets/quote?tvwidgetsymbol={ticker}', headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        # try:
        print(soup.text)
        profile = soup.find(class_='tv-symbol-profile__description').text
        await ctx.send(profile)
        # except AttributeError:
            # await ctx.send(f'Investopedia does not have a description for {ticker}')
        await message.delete()



def setup(bot):
    bot.add_cog(StockCommands(bot))
