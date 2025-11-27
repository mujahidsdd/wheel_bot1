import discord
from discord.ext import commands
import os
import asyncio
from aiohttp import web

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = "!"
PORT = int(os.getenv('PORT', 8000))

class LuckWheelBotMain(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)
        self.ready = False

    async def setup_hook(self):
        await self.load_cogs()
        await self.tree.sync()
        print("✅ تم مزامنة أوامر Slash")

    async def load_cogs(self):
        """Load all cogs from cogs directory"""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ تم تحميل Cog: {filename[:-3]}")
                except Exception as e:
                    print(f"❌ خطأ في تحميل {filename}: {e}")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print(f"✅ Bot Online: {self.user}")
            print(f"📊 Guilds: {len(self.guilds)}")
            await self.change_presence(
                activity=discord.Game(name="عجلة الحظ 🎡 | /spin")
            )
            print("✅ نظام الدورة اليومية جاهز")

async def health_check(request):
    """Health check endpoint for UptimeRobot"""
    return web.json_response({'status': 'ok', 'bot': 'running'})

async def start_web_server():
    """Start aiohttp web server for UptimeRobot ping"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/ping', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"✅ HTTP Server started on port {PORT}")
    return runner

async def main():
    # Start HTTP server for UptimeRobot
    web_runner = await start_web_server()
    
    async with LuckWheelBotMain() as bot:
        try:
            await bot.start(DISCORD_TOKEN)
        finally:
            await web_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
