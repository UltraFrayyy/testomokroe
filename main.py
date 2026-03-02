import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from moviepy import VideoFileClip, vfx

TOKEN = "8785694262:AAFqKY7TfIy_VF_WE5uY7_-GdDbc51BUsMg"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("видео бо чювак")

@dp.message(F.video | F.document)
async def handle_video(message: Message):
    video_source = message.video if message.video else message.document
    if message.document and not (message.document.mime_type and message.document.mime_type.startswith('video')):
        return

    msg = await message.answer("андрюха пчелокур")
    
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

            clip = clip.with_effects([vfx.Crop(x_center=w/2, y_center=h/2, width=min_side, height=min_side)])
            
            clip = clip.with_effects([vfx.Resize(height=384)])

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
        await message.answer(f"бля ерор: {e}")
        print(f"чеклох: {e}")
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

async def main():
    print("жыв")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
