#!/usr/bin/env python3

import discord
from discord.ext import commands
import time
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, description='WHEN?')

when_list = ['','','','','']
name_list = ['','','','','']
timer_start = time.perf_counter()
when_emoji = '<:when:578647608973852672>'

def reset_list():
    for x, i in enumerate(when_list):
        when_list[x] = ':negative_squared_cross_mark:'
        name_list[x] = ':negative_squared_cross_mark:'

reset_list()


@bot.command()
async def when(ctx):
    global timer_start
    global when_list
    global name_list

    if ctx.message.content == '!when' or ctx.message.content.startswith('!when --add'):
        if ctx.message.content.startswith('!when --add'):
            user = ctx.message.content.split()[-1]
            user_name = '@' + ctx.message.content.split()[-1]
        else:
            user = ctx.message.author.name
            user_name = ctx.message.author.mention

        timer_end = time.perf_counter()

        if timer_end - timer_start > 14400:
            reset_list()
            await ctx.send('List has been reset due to time exceeding 4h')

        timer_start = time.perf_counter()
        
        for x, i in enumerate(when_list):
            if when_list[x].endswith(f'{user}'):
                await ctx.send(f'You are already in the list, baka')
                await ctx.send('\n'.join(when_list))
                return 0

        for x, i in enumerate(when_list):
            if when_list[x].startswith(':negative_squared_cross_mark:'):
                when_list[x] = f':green_square: {user}'
                name_list[x] = f':green_square: {user_name}'
                break

                
        if all(item.startswith(':green_square:') for item in when_list):
            await ctx.send(when_emoji)
            await ctx.send('\n'.join(name_list))
            reset_list()
        else:
            await ctx.send(when_emoji)
            await ctx.send('\n'.join(when_list))
        

    if ctx.message.content == '!when remove' or ctx.message.content.startswith('!when --remove'):
        if ctx.message.content.startswith('!when --remove'):
            user = ctx.message.content.split()[-1]
            user_name = '@' + ctx.message.content.split()[-1]
        else:
            user = ctx.message.author.name
            user_name = ctx.message.author.mention

        for x, i in enumerate(when_list):
            if user in when_list[x]:
                when_list[x] = ':negative_squared_cross_mark:'
                name_list[x] = ':negative_squared_cross_mark:'
        await ctx.send(f'Get fucked {ctx.message.author.name}\n')
        await ctx.send('\n‎'.join(when_list))

    if ctx.message.content == '!when status':
        await ctx.send('\n‎'.join(when_list))

    if ctx.message.content == '!when ping':
        await ctx.send('\n'.join(name_list))

    if ctx.message.content == '!when reset':
        reset_list()
        await ctx.send(when_emoji)
        await ctx.send('\n‎'.join(when_list))


    if ctx.message.content == '!when help':
        await ctx.send(f'`!when` - Add yourself to the {when_emoji} list\n' \
            f'`!when remove` - Remove yourself from the {when_emoji} list\n' \
            f'`!when reset` - Reset the entire {when_emoji} list\n' \
            f'`!when status` - Print the current status of the {when_emoji} list\n' \
            f'`!when ping` - Ping all the current people in the {when_emoji} list\n' \
            '`!when help` - Prints this help page\n\n' \
            'The list clears itself after 5 people have been added and it pings everyone.\n' \
            'It also clears itself after 4h of nobody adding themselves to the list'
        )


bot.run(os.environ.get('token'))
