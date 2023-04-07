# octa-tg-bot

## how to run

```
python3 -m venv venv
. venv/bin/activate
pip install aiohttp humanize requests-cache pyTelegramBotAPI
export TELEGRAM_BOT_TOKEN=....
./bot.py
```

## docker

```
docker build . --tag octa-tg-bot:0.0.1
```
