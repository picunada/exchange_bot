from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from tortoise.expressions import Q

from bot.buttons.menu import menu, active_menu, check_menu, paid_menu, transaction_completed
from bot.bot import dp, bot
from bot.filters.admin import AdminFilter
from bot.states import Exchange
from core.config import Settings
from core.logger import log
from models import Users, Orders, Status, Banks, Rates, Manager
from utils.check_card_bin import check_bank

dp.filters_factory.bind(AdminFilter)
config = Settings()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Приветствую, {message.from_user.full_name}!\n\n" "Это телеграм бот для совершения "
                         "безналичного обмена гривны на рубль.\n\n""В этом боте вы сможете безопасно обменять гривну "
                         "на "
                         "рубль \n\n""Пожалуйста, ознакомьтесь с инструкцией перед началом обмена. \n\n""Если, "
                         "Вы уже ознакомились, то вперед!\n\n""⬇️⬇️⬇️  Начать обмен  ⬇️⬇️⬇️", reply_markup=menu,
                         parse_mode="Markdown")
    print(message.from_user.id)
    print(type(message.from_user.id))


@dp.message_handler(Text(equals='Что-то пошло не так, отменяем ❌'), state='*')
@dp.message_handler(Text(equals='Что-то пошло не так, отменяем ❌', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    user_obj = await Users.get_or_none(chat_id=message.chat.id)
    current_state = await state.get_state()
    if current_state is Exchange.payment_process:
        data = await state.get_data()
        user_id = data.get("user_id")
        user_obj = await Users.get(chat_id=user_id)
        bot.send_message(chat_id=user_id, text="К сожалению средства так и не поступили\n\n"
                                               "Если возникли вопросы, с радостью ответим!\n"
                                               "@supportbot")
    order_obj = await Orders.all().order_by("-id").get_or_none(user=user_obj).first()
    if order_obj is not None:
        status_obj, created = await Status.get_or_create(status="Canceled")
        await Orders.filter(id=order_obj.id).update(status=status_obj)
    await state.finish()
    await message.reply('Отменено.', reply_markup=menu)


@dp.message_handler(Text(equals="Начать обмен 💰💰💰"), state=None)
async def start_exchange(message: types.Message):
    n = 1000
    rate_obj = await Rates.all().order_by("-id").first()
    user_obj = await Users.get_or_none(chat_id=message.chat.id)
    if user_obj is None:
        await Users.create(username=message.from_user.username, chat_id=message.chat.id)
    await message.answer(f"Текущий курс - {rate_obj.rate}\n\n" f"*пример*: за {n} гривен вы"
                         f" получите {int(n * rate_obj.rate)} рублей\n\n" "Пожалуйста, введите сумму которую"
                         " вы хотите обменять в гривнах\n"
                         "*минимальная сумма обмена* - 1000 грн\n"
                         "*максимальная сумма обмена* - 29000 грн\n", reply_markup=active_menu,
                         parse_mode="Markdown")
    await Exchange.amount.set()


@dp.message_handler(state=Exchange.amount)
async def get_amount(message: types.Message,
                     state: FSMContext):
    if message.text is None:
        log.error("Message is None!")
    try:
        amount = int(message.text)
        if amount not in range(1000, 29001):
            raise ValueError("Введите количество в диапозоне от 1000 до 29000")
        await state.update_data({
            "amount": amount
        })
        await message.answer("Пожалуйста, введите номер карты, на которую вы хотите получить выплату в рублях",
                             reply_markup=active_menu)
        await Exchange.next()
    except Exception as e:
        await message.answer("Что то пошло не так, попробуйте ввести корректное число")
        await Exchange.amount.set()
        log.error(e)


@dp.message_handler(state=Exchange.card_num)
async def check(message: types.Message,
                state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    card_number = message.text
    await state.update_data({
        "card_number": str(card_number)
    })
    rate_obj = await Rates.all().order_by("-id").first()
    await message.answer("Пожалуйста, проверьте введенные данные!\n\n"
                         f"Отдаете - {amount} грн\n"
                         f"Получаете - {int(amount * rate_obj.rate)} рублей на карту {card_number}",
                         reply_markup=check_menu)
    await state.update_data({
        "user_id": message.from_user.id
    })
    await Exchange.next()


@dp.message_handler(Text(equals="Все верно, готов оплатить! ✅"), state=Exchange.check)
async def admin_link(message: types.Message, state=FSMContext):
    try:
        data = await state.get_data()
        user_id = data.get("user_id")
        amount = data.get("amount")
        card_number = data.get("card_number")
        current_bank = check_bank(card_number)
        user_obj = await Users.get(chat_id=user_id)
        status_obj = await Status.get_or_none(status="New")
        rate_obj = await Rates.all().order_by("-id").first()
        if status_obj is None:
            status_obj = await Status.create(status="New")
        bank_obj = await Banks.get_or_none(bank_name=current_bank)
        if bank_obj is None:
            bank_obj = await Banks.create(bank_name=current_bank)
        await Orders.create(amount_before=amount, amount_after=int(amount * rate_obj.rate), rate=rate_obj,
                            withdraw_card=card_number, user=user_obj, manager=None, bank=bank_obj,
                            status=status_obj)
        count = 0
        admins = await Users.filter(is_admin=True).all()
        print(admins)
        for admin in admins:
            active_orders = await Orders.filter((Q(status=1) | Q(status=2)) & Q(manager=admin)).count()
            print(active_orders)
            if active_orders == 0:
                await bot.send_message(chat_id=admin.chat_id, text=f"@{message.from_user.username}:\n"
                                                                   f"card: {card_number}, amount in UAH: {amount}\n"
                                                                   f"amount in RUB: {int(amount * rate_obj.rate)}")
                await bot.send_message(chat_id=admin.chat_id, text="Отправьте ссылку")
                await state.set_state_to_user(user=admin.chat_id, chat=admin.chat_id, state=Exchange.admin_link)
                await state.set_data_to_user(user=admin.chat_id, chat=admin.chat_id, data=data)
                count += 1
        if count == 0:
            await message.answer("Подождите пару минут, в данный момент все модераторы заняты")
        else:
            await message.answer("В течениие 10 минут прийдет ссылка для оплаты", reply_markup=active_menu)
    except Exception as e:
        log.error(e)


@dp.message_handler(state=Exchange.admin_link, is_admin=True)
async def payment_process(message: types.Message,
                          state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    admin_obj = await Users.get(chat_id=message.from_user.id)
    user_obj = await Users.get(chat_id=user_id)
    manager_obj = await Manager.get_or_none(user=admin_obj)
    if manager_obj is None:
        manager_obj = await Manager.create(user=admin_obj)
    await Orders.filter(user=user_obj).order_by("-id").first().update(manager=manager_obj)
    await bot.send_message(chat_id=user_id, text="Перейдите по ссылке ниже,"
                                                 " введите данные платежной карты и нажмите оплатить."
                                                 " После успешной оплаты вам прийдет оповещение\n\n",
                           parse_mode="HTML")
    await bot.send_message(chat_id=user_id, text=f"Ваша ссылка для оплаты: {message.text}")
    await bot.send_message(chat_id=user_id, text="<a align=\"center\"> ⚠️Внимание⚠️ </a>\n"
                                                 "Ссылка действительна 15 минут.\n"
                                                 "Если в течении указанного времени вы не смогли оплатить,"
                                                 " обмен отменяется автоматически."
                                                 " Но это не проблема, вы всегда можете оформить новый 😉",
                           parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
    await Exchange.next()
    await payment_accept(message, state)


@dp.message_handler(state=Exchange.admin_check, is_admin=True)
async def payment_accept(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    try:
        user_obj = await Users.get(chat_id=user_id)
        status_obj, created = await Status.get_or_create(status="Processed")
        await Orders.filter(user=user_obj).order_by("-id").first().update(status=status_obj)
        order_obj = await Orders.filter(user=user_obj).order_by("-id").prefetch_related("manager").first()
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Ссылка отправлена пользователю, id заказа: {order_obj.id},"
                                    f" номер карты: {order_obj.withdraw_card}\n"
                                    f"После оплаты пользователя нажмите на кнопку\n"
                                    f"Пользователь оплатил✅", reply_markup=paid_menu)
        await Exchange.next()
    except Exception as e:
        log.error(e)


@dp.message_handler(Text(equals="Пользователь оплатил✅"), state=Exchange.payment_process, is_admin=True)
async def payment_check(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await Orders.filter(user=user_id).order_by("-id").first().update(is_paid=True)
    await bot.send_message(chat_id=user_id, text="Средства получены!\n"
                                                 "Делаем вам перевод!")
    await message.answer("После успешного перевода клиенту нажмите на кнопку перевод завершен",
                         reply_markup=transaction_completed)
    await Exchange.next()


@dp.message_handler(Text(equals="Перевод завершен"), state=Exchange.transaction_end)
async def transaction_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    user_obj = await Users.get(chat_id=user_id)
    order_obj = await Orders.all().order_by("-id").get_or_none(user=user_obj).first()
    await bot.send_message(chat_id=user_id, text=f"Обмен завершен успешно!\n"
                                                 f"На карту {order_obj.withdraw_card}"
                                                 f" отправлено {order_obj.amount_after} рублей.", reply_markup=menu)

    status_obj, created = await Status.get_or_create(status="Finished")
    await Orders.filter(id=order_obj.id).update(status=status_obj)
    await state.set_state_to_user(user=user_id, chat=user_id, state=None)
    data.clear()
    active_orders = await Orders.filter((Q(status=1) | Q(status=2)) & Q(manager=None)).get_or_none()
    if active_orders is None:
        await message.answer("Отлично, ожидайте следущего заказа", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        new_order = await active_orders.first()
        await state.reset_data()
        await state.set_state(Exchange.admin_link)
        await state.update_data({
            "user_id": new_order.user.chat_id
        })


@dp.message_handler(commands="get_order_status")
async def get_order_status(message: types.Message):
    try:
        user_obj = await Users.get_or_none(chat_id=message.chat.id)
        if user_obj is None:
            await message.answer("Нажмите кнопку exchange")
            return
        order_obj = await Orders.get_or_none(user=user_obj).prefetch_related('status')
        current_order = await Orders.from_tortoise_orm(order_obj)
        await message.answer(f"Статус вашего заказа({current_order.id}): {order_obj.status.status}")
    except Exception as e:
        log.error(e)
