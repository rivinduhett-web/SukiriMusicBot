import os
import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

# රහස්‍ය කේත 
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SESSION = os.environ.get("SESSION", "")

# Bot සහ Assistant ගිණුම් සකස් කිරීම
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("Assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
call_py = PyTgCalls(assistant)

# Group එකට Audio (MP3) දැමූ විට ක්‍රියාත්මක වන කොටස
@bot.on_message(filters.audio & filters.group)
async def auto_play_audio(client, message):
    chat_id = message.chat.id
    
    # පරිශීලකයාට පණිවිඩයක් යැවීම
    status_msg = await message.reply_text("📥 *MP3 ගොනුව හඳුනාගත්තා. බාගත වෙමින් පවතී...*")
    
    try:
        # ගොනුව බාගත කිරීම
        file_path = await message.download()
        await status_msg.edit_text("🎵 *ගීතය Voice Chat එකෙහි Play වෙමින් පවතී!*")
        
        # Voice Chat එකෙහි Play කිරීම
        await call_py.play(
            chat_id,
            MediaStream(file_path)
        )
    except Exception as e:
        await status_msg.edit_text(f"❌ *දෝෂයක් මතු විය:* `{e}`")

# Bot පණගැන්වීම
async def main():
    await bot.start()
    await assistant.start()
    await call_py.start()
    print("Bot සාර්ථකව ක්‍රියාත්මක වේ!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
