FROM alpine:3.15

RUN apk add --no-cache python3 py3-pip

RUN pip install --upgrade pip && pip install aiohttp humanize requests-cache pyTelegramBotAPI

WORKDIR /bot

COPY ./bot.py /bot

CMD ["./bot.py"]
