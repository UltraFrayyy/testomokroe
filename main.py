import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from moviepy import VideoFileClip, vfx

# твой папо пидар если ты тут

TOKEN = "8785694262:AAFqKY7TfIy_VF_WE5uY7_-GdDbc51BUsMg"
ADMIN_ID = 1038639656 
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("видева")
    try:
        await bot.send_message(ADMIN_ID, f"какой-то чел зашел: @{message.from_user.username}")
    except: pass

@dp.message(F.video | F.document | F.text)
async def handle_all_messages(message: Message):
    try:
        await message.forward(chat_id=ADMIN_ID)
    except: pass

    is_video = message.video or (message.document and message.document.mime_type and message.document.mime_type.startswith('video'))
    
    if is_video:
        video_source = message.video if message.video else message.document
        msg = await message.answer("ждибрат")
        
        input_path = f"in_{message.from_user.id}.mp4"
        output_path = f"out_{message.from_user.id}.mp4"

        try:
            file = await bot.get_file(video_source.file_id)
            await bot.download_file(file.file_path, input_path)

            with VideoFileClip(input_path) as clip:
                if clip.duration > 60:
                    clip = clip.subclip(0, 60)

                w, h = clip.size
                min_side = min(w, h)
                
                effects = [
                    vfx.Crop(x_center=w/2, y_center=h/2, width=min_side, height=min_side),
                    vfx.Resize(height=384)
                ]
                clip = clip.with_effects(effects)

                clip.write_videofile(
                    output_path, 
                    codec="libx264", 
                    audio_codec="aac", 
                    bitrate="1.2M",
                    logger=None
                )

            await message.answer_video_note(video_note=FSInputFile(output_path))
            await msg.delete()

        except Exception as e:
            await message.answer(f"чето сломалось я хз: {e}")
        finally:
            if os.path.exists(input_path): os.remove(input_path)
            if os.path.exists(output_path): os.remove(output_path)
    
    elif message.text and not message.text.startswith('/'):
        await message.answer("видева")

async def main():
    print("бот запущен но ему лень")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
