import discord, requests, os, random, hashlib, cryptocode
from bs4 import BeautifulSoup
from discord_components import Button
from discord.ext import commands
from dotenv import load_dotenv
from replit import db
from random import randrange
from time import perf_counter
from discord.errors import NotFound

load_dotenv()


class AnonCommands(commands.Cog, name='Anon Commands'):
    '''Anon commands'''
    def __init__(self, bot):
        self.bot = bot

    async def anon_message_function(self, bot, ctx, channel, message_text, vanon_boolean, vanon_id, vanon_password, ranon_id):
        try:
            channel=int(channel)
        except ValueError:
            channel = channel.lower()
            channel_keys = {
                'confessions': 833788929525678149,
                'confession': 833788929525678149,
                'confess': 833788929525678149,
                'c': 833788929525678149,
                'horny-confessions': 883921884230602762,
                'horny-confession': 883921884230602762,
                'hc': 883921884230602762,
                'bots': 787079371454283796,
                'b': 787079371454283796,
                'lgbtq': 787562168852676629,
                'politics-and-current-events': 796518787628400660,
                'politics': 796518787628400660,
                'pce': 796518787628400660,
                'ask-rice': 787077776724590663,
                'ask': 787077776724590663,
                'ar': 787077776724590663,
                'pre-health': 796589258382114836,
                'health': 796589258382114836,
                'ph': 796589258382114836,
                'class-rants': 882734037762977823,
                'rants': 882734037762977823,
                'cr': 882734037762977823,
                }
            if channel in channel_keys:
                channel = channel_keys[channel]
            if channel not in [
                    833788929525678149, 787079371454283796,
                    787077776724590663, 796589258382114836,
                    787562168852676629, 796518787628400660,
                    882734037762977823, 883921884230602762,
            ]:  # these channels have been chosen so there is no spamming
                await ctx.send('You cannot send messages in that channel')
                return
        message_channel = bot.get_channel(channel)
        anon_message = message_text
        anon_message += f'\n\n**All confessions are anonymous. Rice Bot has public code which is available using the ^code command**'
        if vanon_boolean:
            db_key = 'anon_password_' + vanon_id
            if db_key not in db:
                await ctx.send(
                    'A message of that id has not been sent anonymously with Rice Bot.'
                )
                return
            hashed_password = db[db_key]
            hashed_vanon_password = hashlib.sha256(
                vanon_password.encode()).hexdigest()
            if hashed_password == hashed_vanon_password:
                await ctx.send('Your password matches!')
                try:
                    msg = await message_channel.fetch_message(int(vanon_id))
                except NotFound:
                    await ctx.send(
                        'Message not sent: a verified message must be sent in the same channel as the original message.'
                    )
                    return
                msg_number = msg.embeds[0].title[12:20]
                msg_number_correct = [
                    character for character in msg_number
                    if character.isdigit()
                ]
                anon_message = f'*This message has been verified to be from the author of #{"".join(msg_number_correct)}*\n\n' + anon_message
                # https://discord.com/channels/787069146852360233/{channel}/{vanon_id}
            else:
                await ctx.send('Your password does not match.')
                return
        # messages = [
        #     anon_message[i:i + 4096] for i in range(0, len(anon_message), 4096)
        # ]
        # embeds = []
        colors = [
            random.randrange(0, 255),
            random.randrange(0, 255),
            random.randrange(0, 255)
        ]
        message_number = db["anon_message"] + db["frq_anon_message"] + db["frq_verified_anon_message"] + db['frq_reply_anon_message']
        if vanon_boolean:
            message_number -= 1
        # for i, anon_message_part in enumerate(messages):
        #     title = f'Anon message #{message_number} Part {i+1} of {len(messages)}'
        #     embeds.append(
        #         discord.Embed(title=title,
        #                       description=anon_message_part,
        #                       color=discord.Color.from_rgb(
        #                           colors[0], colors[1], colors[2])))
        # for embed in embeds:
        #     if vanon_boolean:
        #         channel_message_sent = await msg.reply(embed=embed)
        #     else:
        #         channel_message_sent = await message_channel.send(embed=embed)
        title = f'Anon message #{message_number}'
        if vanon_boolean:
            channel_message_sent = await msg.reply(title)
        elif ranon_id != '':
            msg = await message_channel.fetch_message(int(ranon_id))
            channel_message_sent = await msg.reply(title)
        else:
            channel_message_sent = await message_channel.send(title)
        allowed_chars = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        password = ''.join(random.choice(allowed_chars) for x in range(10))
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db['anon_password_' + str(channel_message_sent.id)] = hashed_password
        channel_id = channel_message_sent.id
        if vanon_boolean:
            channel_id = vanon_id
        await ctx.send(f'**Message #{message_number} sent**')
        message_instructions = f'For future verification, use ```^vanon {channel_message_sent.id} {password} {channel} message text``` to send a verified message from the author of #{message_number}'
        if vanon_boolean:
            message_instructions += f'\n\nTo view the inbox for this message use the password from your previous verified message ```^ianon {channel_id} previous_password```'
        else:
            message_instructions += f'\n\nTo view the inbox for this message use ```^ianon {channel_id} {password}```'
        
        await ctx.send(message_instructions)
        anon_message += f'\nUsers can be added to this inbox through ```^canon {channel_id}```'
        embed = discord.Embed(title=title,
                            description=anon_message,
                            color=discord.Color.from_rgb(
                                colors[0], colors[1], colors[2]))
        await channel_message_sent.edit(content='', embed=embed)

    @commands.command(aliases=['anon', 'confess'])
    async def anon_message(self, ctx, channel, *, arg):
        '''
        Send an anonymous message
        '''
        await self.anon_message_function(self.bot, ctx, channel, arg, False, 0, '', '')

    @commands.command(aliases=['vanon'])
    async def verified_anon_message(self, ctx, message_id, password, channel,*, arg):
        '''
        Send a verified anonymous message to the same channel as a previous anonymous message
        '''
        await self.anon_message_function(self.bot, ctx, channel, arg, True, message_id, password, '')

    @commands.command(aliases=['ranon'])
    async def reply_anon_message(self, ctx, channel, message_id,*, arg):
        '''
        Send an anonymous message to the same channel as a previous anonymous message 
        '''
        await self.anon_message_function(self.bot, ctx, channel, arg, False, 0, '', message_id)

    @commands.command(aliases=['canon', 'anonc'])
    async def connect_anonymous(self, ctx, message_id):
        '''
        Add your username to the contact inbox for a specific message
        '''
        if 'anon_password_' + message_id not in db:
            await ctx.send(
                'A message of that id has not been sent anonymously with Rice Bot.'
            )
            return
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        await ctx.send(
            f'Please confirm that you wish to be added to the inbox for {message_id} by responding with **Y**.\n\nYour username will be visible to the author of {message_id} if they check their inbox. Your username will also be encrypted and saved in the Rice Bot database using symmetric-key encryption.'
        )
        msg = await self.bot.wait_for('message', check=check, timeout=30)
        if msg.content.lower() in ['yes', 'y']:
            added = True
            db_key = f'anon_inbox_{message_id}'
            author_string = cryptocode.encrypt(str(ctx.author).replace('#', ''), os.getenv('simplecrypt-key'))
            if db_key in db:
                unencrypted_db = [cryptocode.decrypt(user, os.getenv('simplecrypt-key')) for user in db[db_key]]
                unencrpyted_author_string = str(ctx.author).replace('#', '')
                if unencrpyted_author_string in unencrypted_db:
                    db_value = db[db_key]
                    del db_value[unencrypted_db.index(unencrpyted_author_string)]
                    db[db_key] = db_value
                    added = False
                else:
                    db_value = db[db_key]
                    db_value.append(author_string)
                    db[db_key] = db_value
            else:
                db[db_key] = [author_string]
            if added:
                await ctx.send(
                    f"{ctx.author} has been added to the inbox for {message_id}.")
            else:
                await ctx.send(
                    f"{ctx.author} has been removed from the inbox for {message_id} because you were already in it.")
        else:
            await ctx.send(
                f"{ctx.author} has not been added to the inbox for {message_id}.")
                    

    @commands.command(aliases=['ianon'])
    async def anonymous_inbox(self, ctx, message_id, password):
        '''
        Add your username to the contact inbox for a specific message
        '''
        db_key = 'anon_password_' + message_id
        if db_key not in db:
            await ctx.send(
                'A message of that id has not been sent anonymously with Rice Bot.'
            )
            return
        hashed_password = db[db_key]
        hashed_anon_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == hashed_anon_password:
            await ctx.send('Your password matches!')
            db_key_inbox = f'anon_inbox_{message_id}'
            if db_key_inbox in db:
                users = [cryptocode.decrypt(user, os.getenv('simplecrypt-key')) for user in db[db_key_inbox]]
                users = [f'{user[:-4]}#{user[-4:]}' for user in users]
                message_to_send = '\n'.join(users)
                message_to_send += '\n\n**The users in your inbox do not know if you check your inbox. It is your choice to contact them.\nAll confessions are anonymous. Rice Bot has public code which is available using the ^code command**'
                colors = [
                    random.randrange(0, 255),
                    random.randrange(0, 255),
                    random.randrange(0, 255)
                ]
                await ctx.send(embed=discord.Embed(title=f'Inbox for Message {message_id}',
                              description=message_to_send,
                              color=discord.Color.from_rgb(
                                  colors[0], colors[1], colors[2])))
            else:
                await ctx.send(
                    f'There are no users in the inbox for {message_id}')
        else:
            await ctx.send('Your password does not match.')
            return


def setup(bot):
    bot.add_cog(AnonCommands(bot))
