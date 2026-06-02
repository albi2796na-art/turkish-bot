from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "8939803597:AAFgz50C5BUzEyY0k8Sc6p-pBoECpytACpA"
PDF_FILE_ID = "BQACAgQAAxkBAAMnah3YQdFoF9vViIDbbnOWXKpqf1UAAnUgAAKxEelQMVq28nvTPzQ7BA"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇹🇷 Купить гайд")],
            [KeyboardButton(text="✨ Что внутри?")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Нужен гайд «300 турецких фраз»? Жми кнопку ниже!",
        reply_markup=get_keyboard()
    )

@dp.message(F.text == "✨ Что внутри?")
async def what_inside(message: Message):
    await message.answer(
        "📖 Гайд «300 турецких фраз» включает:\n\n"
        "🛍 Шопинг и торг на рынке\n"
        "☕ Кафе и рестораны\n"
        "🚕 Такси и транспорт\n"
        "🏨 Аренда жилья\n"
        "🏛 Официальные инстанции и ВНЖ\n"
        "💊 Здоровье и аптека\n\n"
        "Все фразы с переводом и транскрипцией!",
        reply_markup=get_keyboard()
    )

@dp.message(F.text == "🇹🇷 Купить гайд")
async def buy_guide(message: Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="📖 300 турецких фраз",
        description="Фразы для шопинга, кафе, такси, ВНЖ и больницы. Сразу после оплаты получишь PDF!",
        payload="guide_300_phrases",
        currency="XTR",
        provider_token="",
        prices=[LabeledPrice(label="Гайд 300 фраз", amount=75)],
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    await message.answer("✅ Оплата прошла! Отправляю гайд...")
    await bot.send_document(
        chat_id=message.chat.id,
        document=PDF_FILE_ID,
        caption="📖 Твой гайд «300 турецких фраз». Приятного изучения! 🇹🇷"
    )

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
