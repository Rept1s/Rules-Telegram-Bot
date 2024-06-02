import asyncio
from environs import Env
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


class AlbumHandler:
    def __init__(self):
        self.album_end_tracker = defaultdict(list)
        self.album_locks = defaultdict(asyncio.Lock)

    async def check_album_and_send(self, message: Message):
        """
        Проверяет, является ли альбомом, для того чтобы в дальнейшем не дублировать сообщение с просьбой подписаться/принять правила.
        """
        if message.media_group_id:
            self.album_end_tracker[message.media_group_id].append(message.message_id)

            async with self.album_locks[message.media_group_id]:
                await asyncio.sleep(4)
                if self.album_end_tracker[message.media_group_id][-1] == message.message_id:

                    for msg_id in self.album_end_tracker[message.media_group_id]:
                        await message.bot.delete_message(message.chat.id, msg_id)
                    del self.album_end_tracker[message.media_group_id]
                    del self.album_locks[message.media_group_id]
                    await answer_message(message)
        else:
            await message.delete()
            await answer_message(message)


async def first_name(message: Message):
    """
        Проверяет на наличие имени/юзернейма для дальнейшего обращения по имени/юзернейма.
    """
    if message.from_user.first_name or message.from_user.full_name or message.from_user.username is not None:
        return (message.from_user.first_name + ',' or message.from_user.full_name + ','
                or message.from_user.username + ',')
    else:
        return 'Пользователь!'


async def answer_message(message: Message):
    """
        Просьба перейти в бот и принять правила/подписаться.
    """
    await message.bot.restrict_chat_member(message.chat.id, message.from_user.id, permissions=ChatPermissions(),
                                           until_date=datetime.timedelta(minutes=1))
    send_answer = await answer_message_check(message)
    await asyncio.sleep(180)  # 3 минут ожидания, далее очистка для удаления лишнего спама
    await send_answer.delete()


async def answer_message_check(message):
    if await select_check_id(message.from_user.id):
        return await message.answer(
            '<a href="tg://user?id=' + str(message.from_user.id) + '">' + str(await first_user_name(message.from_user))
            + '</a>' + ", вам необходимо подписаться на все каналы проекта, чтобы писать в группе. 📝",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                text="♻️ Подписаться", url=Env().str("INVITE_LINK_BOT"))]]))
    return await message.answer(
        '<a href="tg://user?id=' + str(message.from_user.id) + '">' + str(
            await first_user_name(message.from_user)) + '</a>' +
        ", для доступа в группу необходимо принять пользовательское соглашение группы в боте @"
        + Env().str("BOT_USERNAME") + ". 📝",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
            text="📖 Прочитать соглашение", url=Env().str("INVITE_LINK_BOT"))]]))


async def subscribe_direct_message(message: Message):
    """
        Просит подписаться, если пользователь не подписан.
    """
    await message.answer("Подпишитесь на каналы, чтобы использовать бота и писать в чаты",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="Подписаться на канал", url=link)] for link in
                             Env().list("INVITE_LINK_CHANNEL")] +
                             [[InlineKeyboardButton(text="♻️ Подписался", callback_data="subscribed")]]))


async def rules_step(message: Message):
    """
        Просит согласиться с правилами.
    """
    await message.answer('📝 Пожалуйста, прочтите пользовательское соглашение',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="📖 Пользовательское соглашение", url=Env().str("LINK_RULES"))],
                             [InlineKeyboardButton(text="✅ Согласен", callback_data="access_granted")],
                         ]))


async def access_granted(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Добро пожаловать! 🎉')


async def start_next_step(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await rules_step(call.message)


async def answer_not_subscribe(call: CallbackQuery):
    await call.answer()
    answer = await call.message.answer('Вы не подписались на каналы!')
    await asyncio.sleep(60)
    await answer.delete()
