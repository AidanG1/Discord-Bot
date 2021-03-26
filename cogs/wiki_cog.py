import discord, requests, datetime, dateutil.relativedelta
from discord.ext import commands

class WikiCommands(commands.Cog, name='Wikipedia Commands'):
    '''Wikipedia commands'''

    def __init__(self, bot):
        self.bot = bot

    def get_wiki(self, ctx, url, title, count):
        count = int(count)
        if count < 3:
            count = 3
        headers = {
            'User-Agent': 'Discord Bot/0.1 requests',
        }
        r = requests.get(url, headers=headers)
        articles = r.json()['items'][0]['articles']
        pages = ['']
        views = ['']
        i = 0
        for article in articles[:count]:
            if len(pages[i]) + len(views[i]) > 1024:
                i += 1
                pages.append('')
                views.append('')
            if article['article'] not in ['Main_Page', 'Special:Search']:
                pages[
                    i] += f"[{article['article']}]({'https://wikipedia.org/wiki/' + article['article']})\n"
                views[i] += f"{article['views']:,}\n"

        with open('slurs_to_ban.txt') as f:
            text = f.read()
            embeds = []
            for index in pages:
                embeds.append(
                    discord.Embed(title=title, color=discord.Color.blurple()))
            words_to_ban = text.split(',')
            for word in words_to_ban:
                for page in pages:
                    word = word.strip()
                    wtr = word[0]
                    for i in range(len(word) - 1):
                        wtr += '*'
                    page = page.replace(word, wtr, 1)
                    word = word.title()
                    wtr = word[0]
                    for i in range(len(word) - 1):
                        wtr += '*'
                    page = page.replace(word, wtr, 1)
            for i in range(len(pages)):
                embeds[i].add_field(name='Page Title', value=pages[i], inline=True)
                embeds[i].add_field(name='Views', value=views[i], inline=True)
            parts = len(embeds)
            for i in range(len(embeds)):
                embeds[i].title += f', part {i+1} of {parts}'
            return embeds


    @commands.command(aliases=['wiki'])
    async def wikipedia_most_viewed(self, ctx, count='15'):
        '''
        Get the most visited wikipedia pages yesterday
        '''
        today = datetime.datetime.today() - datetime.timedelta(hours=32)
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}"
        embeds = self.get_wiki(
            ctx, url,
            f"Most Viewed Wikipedia Pages On {today.strftime('%Y')}/{today.strftime('%m')}/{today.strftime('%d')}",
            count)
        for embed in embeds:
            await ctx.send(embed=embed)


    @commands.command(aliases=['wikim'])
    async def wikipedia_most_monthly(self, ctx, count='15'):
        '''
        Get the most visited wikipedia pages last month
        '''
        today = datetime.datetime.today() - datetime.timedelta(
            hours=32) - dateutil.relativedelta.relativedelta(months=1)
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{today.strftime('%Y')}/{today.strftime('%m')}/all-days"
        embeds = self.get_wiki(
            ctx, url,
            f"Most Viewed Wikipedia Pages Over {today.strftime('%Y')}/{today.strftime('%m')}",count)
        for embed in embeds:
            await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(WikiCommands(bot))

