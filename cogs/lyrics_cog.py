import discord, requests, os, random
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from replit import db
from random import randrange
from time import perf_counter
from re import sub

load_dotenv()


class LyricsCommands(commands.Cog, name='Lyrics Commands'):
    '''Lyrics commands'''
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(aliases=['cs'])
    async def change_song(self, ctx, *, arg):
        '''
        Change song lyrics
        '''
        r = requests.get(f'https://lyricsfa.com/?s={arg}').text
        soup = BeautifulSoup(r, 'html.parser')
        try:
            song_url = soup.find(id='main-content').article.a['href']
            url_found = True
        except AttributeError:
            await ctx.send(f'No results found for {arg}')
        if url_found:
            r = requests.get(song_url).text
            soup = BeautifulSoup(r, 'html.parser')
            page = soup.find(class_='entry-single')
            lyrics = ''
            first_tag = True
            for tag in page:
                if tag.name == 'p':
                    if len(tag.find_all('a')) > 0:
                        break
                    if first_tag:
                        first_tag = False
                    elif tag.name is not None:
                        if tag.name == 'p':
                            lyrics += tag.text
            lyrics = sub("[\(\[].*?[\)\]]", "", lyrics) # https://stackoverflow.com/questions/14596884/remove-text-between-and
            # self.bot.lyrics = lyrics
            lyrics_to_send = lyrics.replace('\n\n','\n')
            lyrics_to_split = lyrics.replace('\n',' ')
            title = soup.find(class_='entry-title').text
            self.bot.song_title = title
            self.bot.lyrics_list = lyrics_to_split.split(' ')[1:]
            self.bot.lyrics_position = 0
            self.bot.song_length = len(self.bot.lyrics_list)
            self.bot.previous_lyric = ''
            await ctx.send('Song set to: ' + title)

    @commands.command(aliases=['lg', 'l'])
    async def lyrics_guess(self, ctx, *, guess):
        db_name = 'lg_' + str(ctx.message.author).replace('#', '')
        characters_to_remove = [',', ';', '-', '?', '!', '.', '*', '|', '(', ')', '[', ']', '{', '}', "'", '"','.', "'", "`", '’']
        current_lyric = self.bot.lyrics_list[self.bot.lyrics_position]
        lyric_to_guess = current_lyric
        for character in characters_to_remove:
            lyric_to_guess = lyric_to_guess.replace(character, '')
        if guess.lower() == lyric_to_guess.lower():
            self.bot.lyrics_position += 1
            await ctx.send(f'Correct! {self.bot.song_title} is {round(100 * self.bot.lyrics_position/self.bot.song_length,2)}% done')
            if db_name in db:
                db[db_name] = {'correct': db[db_name]['correct'] + 1, 'incorrect': db[db_name]['incorrect']}
            else:
                db[db_name] = {'correct': 1, 'incorrect': 0}
            self.bot.previous_lyric = current_lyric
        elif guess.lower() == 'i_g_u' or guess.lower() == 'i_give_up':
            await ctx.send('The correct lyric is ' + current_lyric)
            self.bot.previous_lyric = current_lyric
            self.bot.lyrics_position += 1
            if db_name in db:
                db[db_name] = {'correct': db[db_name]['correct'], 'incorrect': db[db_name]['incorrect'] + 1}
            else:
                db[db_name] = {'correct': 1, 'incorrect': 0}
        else:
            await ctx.send('Incorrect guess. If you want to give up send "^l  i_g_u"')
            if db_name in db:
                db[db_name] = {'correct': db[db_name]['correct'], 'incorrect': db[db_name]['incorrect'] + 1}
            else:
                db[db_name] = {'correct': 1, 'incorrect': 0}

    @commands.command(aliases=['ll'])
    async def lyrics_leaderboard(self, ctx, count='10'):
        '''
        Get the leaderboard of lyrics
        '''
        keys = db.prefix('lg_')
        print(keys)
        keys = sorted(keys, key=lambda x: db[x]['correct'], reverse=True)
        user = ''
        correct = ''
        incorrect = ''
        for key in keys[0:int(count)]:
            user += f"{key[3:]}\n"
            correct += f"{db[key]['correct']}\n"
            incorrect += f"{db[key]['incorrect']}\n"
        if len(user) + len(correct) > 1024:
            await ctx.send(
                'Message too long. Decrease the count for the message to send.')
        else:
            embed = discord.Embed(title='Most Correct Guesses',                          color=discord.Color.gold())
            embed.add_field(name='User', value=user, inline=True)
            embed.add_field(name='Correct', value=correct, inline=True)
            embed.add_field(name='Incorrect', value=incorrect, inline=True)
            await ctx.send(embed=embed)

    @commands.command(aliases=['as'])
    async def active_song(self, ctx):
        '''
        Get the active song
        '''
        try:
            await ctx.send(f'The active song is: {self.bot.song_title}\nThe previous lyric was "{self.bot.previous_lyric}", lyric number {int(self.bot.lyrics_position) + 1}')
        except AttributeError:
            await ctx.send('There is no active song. Use "^cs song title" to add a song.')



def setup(bot):
    bot.add_cog(LyricsCommands(bot))
