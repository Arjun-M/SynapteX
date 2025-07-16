import platform
import psutil
import socket
import datetime
from telethon import events

async def send_system_info(client, event=None):
    try:
        # System Information
        os_info = f"{platform.system()} {platform.release()}"
        architecture = f"{platform.machine()}"
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = "Not available"
        
        # Boot Time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        
        # CPU Information
        cpu_count = {
            'physical': psutil.cpu_count(logical=False),
            'logical': psutil.cpu_count(logical=True)
        }
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_avg = sum(cpu_percent) / len(cpu_percent)
        
        # Memory Information
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Basic Disk Information (root partition only)
        try:
            disk = psutil.disk_usage('/')
        except:
            disk = None

        # Formatting Functions
        def bytes_to_gb(size):
            return size / (1024 ** 3)
        
        def format_time(seconds):
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        
        # Generate Message
        message = "**🖥️ System Status Report**\n\n"
        message += "**⚙️ System Overview**\n"
        message += f"• **OS:** `{os_info}`\n"
        message += f"• **Architecture:** `{architecture}`\n"
        message += f"• **Hostname:** `{hostname}`\n"
        message += f"• **IP Address:** `{ip_address}`\n"
        message += f"• **Boot Time:** `{boot_time.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        message += f"• **Uptime:** `{format_time(uptime.total_seconds())}`\n\n"
        
        message += "**🔢 CPU Statistics**\n"
        message += f"• **Physical Cores:** `{cpu_count['physical']}`\n"
        message += f"• **Logical Cores:** `{cpu_count['logical']}`\n"
        if cpu_freq:
            message += f"• **Frequency:** `{cpu_freq.current:.2f} MHz`\n"
        message += f"• **Total Usage:** `{cpu_avg:.2f}%`\n"
        message += "• **Per Core Usage:**\n"
        for i, percent in enumerate(cpu_percent, 1):
            message += f"  - Core {i}: `{percent:.2f}%`\n"
        message += "\n"
        
        message += "**🧠 Memory Usage**\n"
        message += f"• **RAM Total:** `{bytes_to_gb(ram.total):.2f} GB`\n"
        message += f"• **RAM Used:** `{bytes_to_gb(ram.used):.2f} GB` (`{ram.percent}%`)\n"
        message += f"• **RAM Free:** `{bytes_to_gb(ram.available):.2f} GB`\n"
        if swap.total > 0:
            message += f"• **Swap Total:** `{bytes_to_gb(swap.total):.2f} GB`\n"
            message += f"• **Swap Used:** `{bytes_to_gb(swap.used):.2f} GB` (`{swap.percent}%`)\n"
        
        message += "\n**💾 Disk Information**\n"
        if disk:
            message += f"• **Total Space:** `{bytes_to_gb(disk.total):.2f} GB`\n"
            message += f"• **Used Space:** `{bytes_to_gb(disk.used):.2f} GB` (`{disk.percent}%`)\n"
            message += f"• **Free Space:** `{bytes_to_gb(disk.free):.2f} GB`\n"
        else:
            message += "• Disk information not available\n"
        
        message += "\n**🔄 Synaptex Userbot Status: Operational**"
        
        if event:
            await event.edit(message)
        else:
            await client.send_message("me", message)
            
    except Exception as e:
        error_message = f"⚠️ Error generating system report: `{str(e)}`"
        if event:
            await event.edit(error_message)
        else:
            await client.send_message("me", error_message)


def register(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"\.sys(?:tem)?$"))
    async def handler(event):
        await event.edit("🔄 Gathering system information...")
        await send_system_info(client, event)

    
