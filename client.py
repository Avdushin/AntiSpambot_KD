from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from dotenv import load_dotenv, dotenv_values
import platform, os, re
import DataBase
import datetime, time
# load .env variables
load_dotenv()

config = dotenv_values(".env")

api_id = config.get('API_ID')
api_hash = config.get('API_HASH')
bot_token = config.get('TOKEN_CLIENT')

client = TelegramClient('BOT', api_id, api_hash).start(bot_token=bot_token)


rights = ChatBannedRights(
        until_date=None,
        view_messages=True,
        send_messages=False,
        send_media=False,
        send_stickers=False,
        send_gifs=False,
        send_games=False,
        send_inline=False,
        embed_links=False,
        send_polls=False,
        change_info=False,
        invite_users=False,
        pin_messages=False
    )


@client.on(events.NewMessage)
async def handle_new_message(event):
    day = time.strptime(DataBase.pass_men(chat_id=event.chat_id), r"%Y-%m-%d")
    day2 = time.strptime(datetime.datetime.now().strftime(r'%Y-%m-%d'), r"%Y-%m-%d")
    print(event.chat_id)
    if day >= day2:
        print(1)
        try:
            user_info =  await client(GetFullUserRequest(event.message.from_id.user_id))
            print(event)
            # Check platform
            if platform.system() == "Windows":
                # Windows
                user_bio = user_info.about
                user_bio =  str(user_bio).lower()
            else:
                # Unix
                user_bio = user_info.full_user.about
                user_bio =  str(user_bio).lower()
        except:
            user_bio = None
        
        message = str(event.message.message).lower()
        
        if ("http" in user_bio or "https" in user_bio or "t.me" in user_bio) or ("@" in user_bio or "bot" in user_bio ) or ("http" in message or "https" in message or "t.me" in message) or ("@" in message or "bot" in message ) :
            try:
                await client.delete_messages(event.chat_id, [event.id])
                await client(functions.channels.EditBannedRequest( event.chat_id, event.message.from_id.user_id, rights))
            except:
                    pass
    else:
        pass
    
        

print(f"\nRun OS: {platform.system()}\n")
client.run_until_disconnected()