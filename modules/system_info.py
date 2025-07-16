import platform
import psutil
from telethon import events

async def send_system_info(client, event=None):
    try:
        # Get system information
        os_info = platform.platform()
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage("/")

        message = (
            f"**Synaptex Userbot Started!**\n\n"
            f"**OS:** `{os_info}`\n"
            f"**CPU Usage:** `{cpu_percent}%`\n"
            f"**RAM Usage:** `{ram_info.percent}%` (`{ram_info.used / (1024**3):.2f}GB` / `{ram_info.total / (1024**3):.2f}GB`)\n"
            f"**Disk Usage:** `{disk_info.percent}%` (`{disk_info.used / (1024**3):.2f}GB` / `{disk_info.total / (1024**3):.2f}GB`)\n"
        )

        if event:
            # Edit the message that triggered .sys
            await event.edit(message)
            # print("System info edited in the original message.")
        else:
            # Send to Saved Messages (for startup)
            await client.send_message("me", message)
            # print("System info sent to Saved Messages.")
    except Exception as e:
        print(f"Error sending system info: {e}")

def register(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"\.sys"))
    async def handler(event):
        await send_system_info(client, event)

    # Register a startup hook to send system info when the client connects
    client.add_event_handler(lambda e: send_system_info(client), events.NewMessage(outgoing=True, pattern=r"\.sys"))
