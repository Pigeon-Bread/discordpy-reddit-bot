import praw
import discord, asyncio
import random
from keys import DISC_TOKEN, RED_CLIENT_ID, RED_CLIENT_SCRT
from discord.ext import commands

DISC_PREFIX = "" #Set the prefix

reddit = praw.Reddit(client_id=RED_CLIENT_ID, client_secret=RED_CLIENT_SCRT, user_agent="discord")
bot = commands.Bot(command_prefix=DISC_PREFIX)

"""A command to search for an image within a specified subreddit given"""
@bot.command()
async def search(ctx, sub=None): 
    if sub is not None: #If there is a arg
        finished = False 
        try:
            post = reddit.subreddit(sub).random() # Gets a random post
            if 'https:"//i.redd.it/' in str(post.url): #Checks if it has a media url
                post_url = post.url
            else: #If not tries to get post
                count = 0
                while not finished:
                    if count == 5: #Will try 5 times or will error
                        error_msg = discord.Embed(description=f"""Couldn't find an image in {sub}""")
                        error = await ctx.channel.send(embed=error_msg)
                        await asyncio.sleep(3)
                        await ctx.message.delete()
                        await error.delete()
                        return
                    post = reddit.subreddit(sub).random() #Gets new random post
                    if 'https://i.redd.it/' in str(post.url):
                        post_url = post.url
                        finished = True #If found breaks the loop
                    else:
                        finished = False #Continues loop as not found
                        count += 1
        except: #Post errored meaning the subreddit doesn't exist
            error_msg = discord.Embed(description=f"""Couldn't find subreddit {sub}""")
            error = await ctx.channel.send(embed=error_msg)
            await asyncio.sleep(3)
            await ctx.message.delete()
            await error.delete()
            return

        image = discord.Embed(title=f"""Image from {sub}""", color=0xe74c3c) #Creates the embed
        image.set_image(url=post_url) #Sets the image as the url found
        image.set_footer(text=f"""requested by {ctx.author}""", icon_url=ctx.author.avatar_url)
        image.set_author(name=f"""From Reddit""", icon_url='https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2')
        await ctx.channel.send(embed=image) #Sends the image
        return 
    else: #No subreddit specified error
        error_msg = discord.Embed(description=f"""Subreddit not specified!""")
        error = await ctx.channel.send(embed=error_msg)
        await asyncio.sleep(3)
        await ctx.message.delete()
        await error.delete()
        return

"""A meme command that gets random memes from different subreddits which are set automatically"""
@bot.command()
async def meme(ctx):
    MEME_SUBS = ["""INSERT MEME SUBS HERE"""]
    found = False
    while not found:
        post = reddit.subreddit(random.choice(MEME_SUBS)).random()
        try:
            if 'https://i.redd.it/' in str(post.url):
                meme_url = post.url
                found = True
            else:
                found = False
        except:
            found = False
    meme_img = discord.Embed(title='M E M E', color=0xe74c3c)
    meme_img.set_image(url=meme_url)
    meme_img.set_footer(text=f"""requested by {ctx.author}""", icon_url=ctx.author.avatar_url)
    meme_img.set_author(name=f"""From Reddit""", icon_url='https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2')
    await ctx.channel.send(embed=meme_img)
    return

bot.run(DISC_TOKEN)
