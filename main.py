from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import config as Config
import csv

client = TelegramClient(f'{Config.PHONE_NUMBER}.session', Config.TELEGRAM_API_ID, Config.TELEGRAM_API_HASH)

async def get_subscribers(channel_link):
    channel = await client.get_entity(channel_link)

    subscribers = []

    offset = 0
    limit = 100
    while True:
        participants = await client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))

        if not participants.users:
            break

        for user in participants.users:
            subscribers.append({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name
            })

        offset += len(participants.users)

    with open('subscribers.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['username', 'first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(subscribers)

    print("Subs saved in subscribers.csv")

async def main():
    channel_link = input("Enter YOUR channel link: ")
    await get_subscribers(channel_link)

client.start(phone=Config.PHONE_NUMBER)

with client:
    client.loop.run_until_complete(main())
