import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from web_scraping import get_content, get_tarot_content , horoscope_signs
from utils import format_embed , format_horoscope_embed
import random

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix= "-" , intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    get_content()
    get_tarot_content()

@bot.command()
async def tarot(ctx):
    tarot_cards = get_tarot_content()
    random_card = random.choice(tarot_cards)
    embed = format_embed(random_card)
    await ctx.send(embed=embed)


@bot.command()
async def burc(ctx, sign):
    sign = sign.lower()
    if sign in horoscope_signs:
        sign_dictionary = get_content()  # Fetch the sign dictionary
        if sign in sign_dictionary:
            embed = format_horoscope_embed(sign_dictionary[sign])
            await ctx.send(embed=embed)
    else:
        await ctx.send("Geçerli bir burç ismi giriniz.")


@tasks.loop(hours=24)
async def my_loop():
    get_content()
    get_tarot_content()
    await bot.change_presence(activity=discord.Game(name=f"-burc <burç ismi>"), status=discord.Status.online)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(TOKEN))
    loop.run_forever()

