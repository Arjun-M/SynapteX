import os
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import importlib.util


SESSION = os.environ.get("TG_SESSION")
API_ID = os.environ.get("TG_API_ID")
API_HASH = os.environ.get("TG_API_HASH")
modules_dir = os.path.join(os.path.dirname(__file__), "modules")


if not API_ID or not SESSION or not API_HASH:
    print("Please set the TG_SESSION , TG_API_ID and TG_API_HASH as environment variables.")
    sys.exit(1)
  

client = TelegramClient( StringSession(SESSION) , API_ID , API_HASH )

async def main():
    print("Synaptex Userbot starting...")
    
    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove .py extension
            module_path = os.path.join(modules_dir, filename)
            
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, "register"):
                module.register(client)
                print(f"Module \'{module_name}\' loaded and registered.")

    await client.start()
    print("Synaptex Userbot started!")
    
    # Send system info to Saved Messages on startup
    if 'system_info' in sys.modules:
        await sys.modules['system_info'].send_system_info(client)

    await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
