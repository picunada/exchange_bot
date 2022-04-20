import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.menu import menu, active_menu
from repository import OrdersRepository, UserRepository, StatusRepository, \
    get_status_repository, get_user_repository, get_orders_repository, get_current_user
from database.connect import database

from bot.bot import dp
from bot.states import Exchange
from core.logger import log
from models import Order, User, Status


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=menu)


@dp.message_handler(commands='cancel', state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    log.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено.', reply_markup=menu)


@dp.message_handler(commands="exchange", state=None)
async def start_exchange(message: types.Message,
                         users: UserRepository = get_user_repository()):
    # try:
    current_user = await get_current_user(int(message.chat.id))
    if current_user is None:
        user = User(
            chat_id=int(message.chat.id),
            username=message.from_user.username,
            is_admin=False,
            is_active=False,
            created_at=datetime.datetime.utcnow()
        )
        await users.create(user)
    if current_user.order_id is not None:
        await message.answer("У вас уже есть заказ")
        return
    await message.answer("Для обмена валюты введите нужное вам количество", reply_markup=active_menu)
    await Exchange.amount.set()


# except Exception as e:
#     log.error(e)


@dp.message_handler(state=Exchange.amount)
async def get_amount(message: types.Message,
                     state: FSMContext):
    if message.text is None :
        log.error("Message is None!")
    try:
        amount = int(message.text)
        await state.update_data({
            "amount": amount
        })
        await message.answer("Введите номер карты для перевода", reply_markup=active_menu)
        await Exchange.next()
    except Exception as e:
        await message.answer("Что то пошло не так, попробуйте ввести корректное число")
        await Exchange.amount.set()
        log.error(e)


@dp.message_handler(state=Exchange.card_num)
async def get_card_number(message: types.Message,
                          state: FSMContext,
                          statuses: StatusRepository = get_status_repository(),
                          orders: OrdersRepository = get_orders_repository(),
                          users: UserRepository = get_user_repository()):
    if message.text is None:
        log.error("Message is None!")
    try:
        current_user = await get_current_user(message.chat.id)
        card_number = int(message.text)
        data = await state.get_data()
        amount = data.get("amount")
        status = Status(
            status="New",
        )
        status = await statuses.create(status)
        order = Order(
            amount=amount,
            rate=0.5,
            withdraw_card=card_number,
            is_paid=False,
            status_id=status.id,
            payment_url="",
            created_at=datetime.datetime.utcnow()
        )
        new_order = await orders.create(order)
        current_user.order_id = new_order.id
        await users.update(id=current_user.id, u=current_user)
        await message.answer(f"Id вашего заказа: {new_order.id}\n"
                             f"Статус вашего заказа: {status.status}", reply_markup=menu)
        await state.finish()
    except Exception as e:
        log.error(e)


@dp.message_handler(commands="get_order_status")
async def get_order_status(message: types.Message,
                           orders: OrdersRepository = get_orders_repository(),
                           statuses: StatusRepository = get_status_repository(),
                           ):
    try:
        current_user = await get_current_user(message.chat.id)
        if current_user is None:
            await message.answer("Нажмите кнопку exchange")

        current_order = await orders.get_by_id(current_user.order_id)
        current_status = await statuses.get_by_id(current_order.status_id)
        await message.answer(f"Статус вашего заказа({current_order.id}): {current_status.status}")

    except Exception as e:
        log.error(e)
