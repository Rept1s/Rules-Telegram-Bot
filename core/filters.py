from environs import Env
from aiogram.filters import BaseFilter
from core.requests import select_check_id, insert_user, update_user
from core.handlers import answer_not_subscribe, access_granted
from aiogram.types import Message, CallbackQuery


class FilterNotUserReg(BaseFilter):
    """
        Проверяет согласие пользователя с правилами.
    """
    async def __call__(self, event: Message) -> bool:
        if await select_check_id(event.from_user.id) is None:
            return True
        else:
            return False


class FilterDateBase(BaseFilter):
    """
        Добавляет пользователя в базу.
    """
    async def __call__(self, event: CallbackQuery) -> bool:
        if await select_check_id(event.from_user.id) is None:
            await insert_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.first_name,
                event.from_user.last_name
            )
        else:
            await update_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.first_name,
                event.from_user.last_name
            )
        return True


class FilterNotUserRegCallBack(BaseFilter):
    """
        Проверяет согласие пользователя с правилами.
    """
    async def __call__(self, event: CallbackQuery) -> bool:
        if await select_check_id(event.from_user.id) is None:
            return True
        else:
            await access_granted(event)
            return False


class FilterUserReg(BaseFilter):
    """
        Проверяет согласие пользователя с правилами.
    """
    async def __call__(self, event: Message) -> bool:
        if await select_check_id(event.from_user.id) is None:
            return False
        else:
            return True


class FilterChatType(BaseFilter):
    """
        Проверяет, является ли чат группой/супергруппой.
    """
    async def __call__(self, event: Message) -> bool:
        if event.chat.type == 'group' or event.chat.type == 'supergroup':
            return True
        else:
            return False


class FilterDirectType(BaseFilter):
    """
        Проверяет, является ли чат приватным.
    """
    async def __call__(self, event: Message) -> bool:
        if event.chat.type == 'private':
            return True
        else:
            return False


class FilterSubChannel(BaseFilter):
    """
        Проверяет, подписан ли пользователь на канал.
    """
    async def __call__(self, event: Message) -> bool:
        try:
            for channel_id in Env().list("CHANNEL_ID"):
                member_status = await event.bot.get_chat_member(channel_id, event.from_user.id)
                if member_status.status in ["left", "kicked"]:
                    return True
            return False
        except Exception as e:
            print(f"Ошибка при проверке статуса подписки: {e}")
            return True


class FilterCallBackChannel(BaseFilter):
    """
        Проверяет, подписан ли пользователь на канал.
    """
    async def __call__(self, event: CallbackQuery) -> bool:
        try:
            for channel_id in Env().list("CHANNEL_ID"):
                member_status = await event.bot.get_chat_member(channel_id, event.from_user.id)
                if member_status.status in ["left", "kicked"]:
                    await answer_not_subscribe(event)
                    return False
            return True
        except Exception as e:
            print(f"Ошибка при проверке статуса подписки: {e}")
            await answer_not_subscribe(event)
            return False


class FilterChatAdmin(BaseFilter):
    """
        Проверяет, является ли пользователь администратором.
    """
    async def __call__(self, event: Message) -> bool:
        if event.from_user.id in event.chat.get_administrators():
            return False
        else:
            return True


class FilterSenderAnonim(BaseFilter):
    """
        Проверяет, отправляет ли пользователь сообщения от имени канала/чата.
    """
    async def __call__(self, event: Message) -> bool:
        if event.sender_chat is not None:
            if event.chat.id == event.sender_chat.id:
                return False
            elif event.sender_chat.type in ('channel', 'group', 'supergroup'):
                print('Написал пользователь от имени канала или чата ' + str(event.sender_chat.id) + ' '
                      + str(event.sender_chat.type) + ' @' + str(event.sender_chat.username))
                await event.bot.delete_message(event.chat.id, event.message_id)
                return False
        else:
            return True
