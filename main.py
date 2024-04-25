import logging
import asyncio
from core.models import async_main
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from core.settings import settings_all
from core.registration import register_reg
from aiogram.client.default import DefaultBotProperties


async def start_bot(bot: Bot):
    await bot.send_message(settings_all().bots.adm_id, text="Бот запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(settings_all().bots.adm_id, text="Бот остановлен")


async def start():
    print('Бот запустился!')
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings_all().bots.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML,
                                                                            link_preview_is_disabled=True))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    await register_reg(dp)
    await async_main()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
