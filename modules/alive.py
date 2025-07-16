from telethon import events
import time

def register(client):
    @client.on(events.NewMessage(outgoing=True, pattern=".alive"))
    async def alive_handler(event):
        start_time = time.time()
        message = await event.edit("Alive!")
        end_time = time.time()
        ping = round((end_time - start_time) * 1000, 2)
        await message.edit(f"Alive and kicking! Ping: `{ping}ms`")
        # print("Alive command executed.")


