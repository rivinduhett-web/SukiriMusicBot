import os
import asyncio
import imageio_ffmpeg
from aiohttp import web
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SESSION = os.environ.get("SESSION", "")

bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("Assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
call_py = PyTgCalls(assistant)

@bot.on_message(filters.audio & filters.group)
async def auto_play_audio(client, message):
    chat_id = message.chat.id
    status_msg = await message.reply_text("📥 *MP3 ගොනුව හඳුනාගත්තා. බාගත වෙමින් පවතී...*")
    try:
        file_path = await message.download()
        await status_msg.edit_text("🎵 *ගීතය Voice Chat එකෙහි Play වෙමින් පවතී!*")
        await call_py.play(chat_id, MediaStream(file_path))
    except Exception as e:
        await status_msg.edit_text(f"❌ *දෝෂයක් මතු විය:* `{e}`")

async def handle(request):
    return web.Response(text="Music Bot is Running Successfully!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    await bot.start()
    await assistant.start()
    await call_py.start()
    print("Bot සාර්ථකව ක්‍රියාත්මක වේ!")
    
    # සදාකාලිකව රන් වීමට ලූප් එකක් තැබීම
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
