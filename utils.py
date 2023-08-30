import discord

def format_embed(item):
    embed = discord.Embed(title=item.name, description=item.description, color=0x00ff00)
    embed.set_image(url=item.image)
    return embed

def format_horoscope_embed(zodiac_sign):
    title = f"Ayın {zodiac_sign.date}. günü için {zodiac_sign.name.upper()} burcu günlük yorumu:"
    embed = discord.Embed(title=title, description=zodiac_sign.description, color=0x6600CC)
    return embed