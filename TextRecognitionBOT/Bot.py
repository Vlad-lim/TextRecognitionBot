import os
from cv2 import resize
import keyboard as nav
import  easyocr
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from config import token, Text_recognition, YouKassaToken
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

#buttons



class FSMStates(StatesGroup):
    Pay_Wait = State()
    Image_get = State()

@dp.message_handler(commands = ['start'])
async def cm_start(message:types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user), reply_markup=nav.mainMenu)


@dp.message_handler(text='Обработка')
async def submonth(message):
    PRICE = types.LabeledPrice(label='Обработка текста на фото', amount=20000)
    await bot.send_invoice(chat_id=message.from_user.id, title = 'Оплата услуги', description='Тестовое описание', payload='month_use', provider_token=YouKassaToken, currency="rub", start_parameter='test_bot', prices=[PRICE], )

    
    


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query:types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT) #УСПЕШНАЯ ОПЛАТА
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_use':
        await message.reply('Теперь отправь мне фотографию, которую хочешь обработать')
        await FSMStates.Pay_Wait.set()

@dp.message_handler(state = FSMStates.Pay_Wait, content_types=['photo'])
async def get_photo(message, state:FSMContext):
    
    file_photo = await bot.get_file(message.photo[-1].file_id)
    filename, fileext = os.path.splitext(file_photo.file_path)
    
    download_photo = await bot.download_file(file_photo.file_path)

    src = 'photos/' + message.photo[-1].file_id + fileext

    with open(src, 'wb') as new_file:
        new_file.write(download_photo.getvalue())

    await message.reply(Text_recognition(src))

    os.remove(src)

    await bot.send_message(message.from_user.id, 'Жри, гнида')

    await state.finish()

        
        
   

if __name__ == '__main__':
    executor.start_polling(dp)