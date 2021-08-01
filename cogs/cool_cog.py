import discord, requests, os, random
from bs4 import BeautifulSoup
from discord_components import Button
from discord.ext import commands
from dotenv import load_dotenv
from replit import db
from random import randrange
from time import perf_counter

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
    async def clear_buttons(self,ctx):
        '''
        Clear active buttons
        '''
        self.bot.button_exists = False
        await ctx.send('Buttons have been cleared. Use ^bt or ^button to make a button.')

    @commands.command(aliases=['bt'])
    async def button(self,ctx):
        '''
        Get a button and see who can click fastest
        '''
        rand = randrange(1,5)
        start_time = perf_counter()
        try:
            button_exists = self.bot.button_exists
        except AttributeError:
            button_exists = False
        if not button_exists:
            m = await ctx.send(
                rand,
                components = [[
                    Button(label = "1", style=randrange(1,4)),
                    Button(label = "2", style=randrange(1,4)),
                    Button(label = "3", style=randrange(1,4)),
                    Button(label = "4", style=randrange(1,4)),
                    Button(label = "5", style=randrange(1,4)),
                ]]
            )
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
                response_time = round(perf_counter() - start_time,2)
                content = f"Correct for {interaction.user}, :white_check_mark: in {response_time} seconds, {speed_word(response_time)}"
                # await interaction.respond(content = f"Correct, :white_check_mark: in {response_time} seconds, {speed_word(response_time)}")
            else:
                content = f"Incorrect for {interaction.user}, :x:"
            await interaction.respond(content = 'Answered')
            await m.edit(
                content,
                components = [[
                    Button(label = "1", style=randrange(1,4), disabled=True),
                    Button(label = "2", style=randrange(1,4), disabled=True),
                    Button(label = "3", style=randrange(1,4), disabled=True),
                    Button(label = "4", style=randrange(1,4), disabled=True),
                    Button(label = "5", style=randrange(1,4), disabled=True),
                ]]
            )
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

    @commands.command(aliases=['anon', 'confess'])
    async def anon_message(self, ctx, channel, *, arg):
        '''
        Send an anonymous message to any channel using the id
        '''
        if channel in ['833788929525678149', '787079371454283796', '787077776724590663', '796589258382114836', '787562168852676629', '796518787628400660']:
            message_channel = self.bot.get_channel(int(channel))
            anon_message = arg
            anon_message += '\n**All confessions are anonymous. Rice bot has public code which is available using the ^code command**'
            messages = [anon_message[i:i+4096] for i in range(0,len(anon_message), 4096)]
            embeds = []
            colors = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)]
            for i, anon_message_part in enumerate(messages):
                title = f'Anon message #{db["anon_message"] + db["frq_anon_message"]} Part {i+1} of {len(messages)}'
                embeds.append(discord.Embed(title=title,
                            description=anon_message_part,
                            color=discord.Color.from_rgb(colors[0], colors[1], colors[2])))
            for embed in embeds:
                await message_channel.send(embed=embed)
            await ctx.send(f'Message #{db["anon_message"] + db["frq_anon_message"] - 1} sent')
        else:
            await ctx.send('You cannot send messages in that channel')



def setup(bot):
    bot.add_cog(CoolCommands(bot))
