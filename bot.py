import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from web_scraping import sign_content_push, tarot_content_push, horoscope_signs
from utils import format_tarot_embed , format_horoscope_embed
from data_models import Model
import random

intents = discord.Intents.all() # This is for the bot to see the members in the server
intents.typing = False 
intents.presences = False 

load_dotenv() 

TOKEN = os.getenv("DISCORD_TOKEN") 

bot = commands.Bot(command_prefix= "-" , intents=intents)  # This is the prefix for the commands
model = Model()
model.create_tables()

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    sign_content_push() # This function scrapes the horoscope content and pushes it to the database
    tarot_content_push() # This function scrapes the tarot content and pushes it to the database
    model.remove_duplicates_if_exists() 

@bot.command()
async def tarot(ctx):
    tarot_cards = model.get_tarot_cards()
    random_card = random.choice(tarot_cards) 
    embed = format_tarot_embed(random_card)
    await ctx.send(embed=embed)


@bot.command()
async def burc(ctx, arg):
    arg = arg.lower()
    if arg in horoscope_signs: # Check if the argument is a valid zodiac sign
        sign = model.get_zodiac_signs()
        for i in sign:
            if i.name == arg: 
                embed = format_horoscope_embed(i)
                await ctx.send(embed=embed)
    else:
        await ctx.send("Geçerli bir burç ismi giriniz. (Türkçe karakter kullanmayınız.)") 

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(TOKEN))
    loop.run_forever()

if __name__ == "__main__": 
    main()
