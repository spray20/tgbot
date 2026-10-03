import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command


TOKEN = "ТОКЕН"

bot = Bot(TOKEN)
dp = Dispatcher()


button = KeyboardButton(text="Случайная статья")

keyboard = ReplyKeyboardMarkup(
    keyboard=[[button]],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот случайных статей Википедии.\n"
        "Нажми кнопку ниже 👇",
        reply_markup=keyboard
    )


@dp.message(F.text == "Случайная статья")
async def random_article(message: Message):

    url = "https://ru.wikipedia.org/api/rest_v1/page/random/summary"

    headers = {
        "User-Agent": "WikiRandomBot/1.0 (exampleemail.com)"
    }

    async with aiohttp.ClientSession() as session:

        async with session.get(
            url,
            headers=headers
        ) as response:

            if response.status != 200:
                await message.answer(
                    f"Ошибка Википедии: {response.status}"
                )
                return

            data = await response.json()

    title = data["title"]

    description = data.get(
        "description",
        "Описание отсутствует."
    )

    article_url = data["content_urls"]["desktop"]["page"]

    text = (
        f"  📖 <b>{title}</b>\n\n"
        f"{description}\n\n"
        f"🔗 {article_url}"
    )

    await message.answer(
        text,
        parse_mode="HTML"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())