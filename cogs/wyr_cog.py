import discord, random
from discord.ext import commands
from cogs.wyr import questions

class WYRCommands(commands.Cog, name='Would You Rather Commands'):
    '''Would you rather commands'''

    def __init__(self, bot):
        self.bot = bot

    def random_question(self, remove_list):
        question = random.choice(questions)
        while question['id'] in remove_list:
            question = random.choice(questions)
        return question


    @commands.command(aliases=['wyr'])
    async def would_you_rather(self, ctx):
        '''
        Get a would you rather
        '''

        message = await ctx.send(self.random_question([])['question'])
        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')


    @commands.command(aliases=['wyrl', 'wyrx'])
    async def would_you_rather_list(self, ctx, remove_list):
        '''
        Get a would you rather and exclude questions from a list
        '''
        remove_list = list(remove_list)
        question = self.random_question(remove_list)
        message = await ctx.send(question['question'])
        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')
        rl = [question['id']]
        number = ''
        for item in remove_list:
            try:
                int(item)
                number += item
            except ValueError:
                if number != '':
                    rl.append(int(number))
                number = ''
        remove_list.append(question['id'])
        await ctx.send('^wyrl ' + str(rl).replace(' ', ''))


def setup(bot):
	bot.add_cog(WYRCommands(bot))