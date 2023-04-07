#!/usr/bin/env python3

from telebot.async_telebot import AsyncTeleBot
import asyncio

from requests_cache import CachedSession
import os
import json
import humanize

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

bot = AsyncTeleBot(TOKEN, parse_mode='MARKDOWN')

session = CachedSession('bot_cache', expire_after=360)

@bot.message_handler(commands=['help'])
async def handle_help(message):
    reply = """
/info   *Common network information*
/mc     *Market Cap*
/ca     *Contract address*
/wp     *White paper*
/links  *Project's links*
/wallet *Wallets*
"""
    await bot.reply_to(message, reply)

@bot.message_handler(commands=['wallet'])
async def handle_wallet(message):
    await bot.reply_to(message, "https://docs.octa.space/cryptocurrency/wallets")

@bot.message_handler(commands=['mc'])
async def handle_mc(message):
    r = session.get('https://api.octa.space/v1/network').json()
    ts = r['blockchain']['total_supply']
    price = r['market_price']
    mc = humanize.intword(ts * price)
    reply = "*{}*".format(mc)
    await bot.reply_to(message, reply)

@bot.message_handler(commands=['contract', 'ca'])
async def handle_contract(message):
    await bot.reply_to(message, "N/A")

@bot.message_handler(commands=['whitepaper', 'wp'])
async def handle_wp(message):
    await bot.reply_to(message, "[https://whitepaper.octa.space](https://whitepaper.octa.space)")

@bot.message_handler(commands=['links'])
async def handle_links(message):
    links = """
*Website*: https://octa.space
*Documentation*: https://docs.octa.space
*Block Explorer*: https://explorer.octa.space
*Console*: https://cube.octa.space
*PoW network statistics*: https://stats.octa.space
*GitHub*: https://github.com/octaspace
*Docker Hub*: https://hub.docker.com/u/octaspace
*Twitter*: https://twitter.com/octa\_space
*BitcoinTalk*: https://bitcointalk.org/index.php?topic=5224155.0
*Medium*: https://medium.com/@octa.space.project 
"""
    await bot.reply_to(message, links)

@bot.message_handler(commands=['info'])
async def handle_info(message):
    r = session.get('https://api.octa.space/v1/network').json()

    difficulty = int(r['blockchain']['difficulty']) / 1024 / 1024
    if difficulty > 1000000:
        difficulty_value = "{0:.2f} Th".format(difficulty / 1024 / 1024)
    elif difficulty > 1000:
        difficulty_value = "{0:.2f} Gh".format(difficulty / 1024)
    else:
        difficulty_value = "{0:.2f} Mh".format(difficulty)

    hashrate = int(r['blockchain']['hashrate']) / 1024 / 1024

    if hashrate > 1000000:
        hashrate_value = "{0:.2f} Th/s".format(hashrate / 1024 / 1024)
    elif hashrate > 1000:
        hashrate_value = "{0:.2f} Gh/s".format(hashrate / 1024)
    else:
        hashrate_value = "{0:.2f} Mh/s".format(hashrate)

    roi = "{0:.2f} %".format(r['roi'])
    market_price = "{0:.5f} USD".format(r['market_price'])

    reply = """
*Nodes*: {}
*VPN AP*: {}
*CPUs*: {}
*GPUs*: {}
*MEM*: {}
*DISK*: {}
*Staked*: {} OCTA
*ROI*: {}
*Era*: {}
*Circulating Supply*: {}
*Market Price*: {}
*Block height*: {}
*Block time*: {}
*Difficulty*: {}
*Hashrate*: {}
""".format(
        r['nodes']['count'],
        r['nodes']['vpn'],
        r['power']['cpus'],
        r['power']['gpus'],
        humanize.naturalsize(r['power']['mem']),
        humanize.naturalsize(r['power']['disk']),
        r['staked'],
        roi,
        r['blockchain']['era'],
        humanize.intcomma(r['blockchain']['total_supply']),
        market_price,
        r['blockchain']['height'],
        r['blockchain']['blocktime'],
        difficulty_value,
        hashrate_value
    )
    await bot.reply_to(message, reply)

asyncio.run(bot.polling())
