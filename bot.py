from pyrogram import Client, filters
from modules.api import make_request
import asyncio



app = Client("my_bot", api_id=17156186, api_hash="c2957f899e43014b76d8df20574764c3", bot_token="6654300611:AAFvy3XLvRUXq7IdyCUhIK_w0XTIGOyX6Vs")

@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.id == 1667320421:
        await client.send_message(chat_id=message.chat.id, text="sadness right?")
        run = True
        while run:
            r = await make_request()
            if r != False:
                await client.send_message(chat_id=message.chat.id, text="ops!")
                for path in r:
                    await client.send_photo(message.chat.id,path)
                    run = False
            else:
                await asyncio.sleep(0.2)

app.run()
