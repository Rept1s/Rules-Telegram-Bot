from aiogram import F
from core.handlers import check_album_and_send, subscribe_direct_message, start_next_step, access_granted, \
    rules_step, check_album_and_subscribe
from core.filters import FilterChatType, FilterChatAdmin, FilterSenderAnonim, FilterDirectType, FilterSubChannel, \
    FilterUserReg, FilterCallBackChannel, FilterNotUserReg, FilterNotUserRegCallBack, FilterDateBase


async def register_reg(dp):
    dp.message.register(check_album_and_send, FilterNotUserReg(), FilterChatType(), FilterChatAdmin(),
                        FilterSenderAnonim())
    dp.message.register(check_album_and_subscribe, FilterUserReg(), FilterSubChannel(), FilterChatType(),
                        FilterChatAdmin(), FilterSenderAnonim())
    dp.message.register(subscribe_direct_message, FilterDirectType(), FilterSubChannel())
    dp.message.register(rules_step, FilterDirectType(), FilterNotUserReg())
    dp.callback_query.register(start_next_step, F.data == 'subscribed', FilterCallBackChannel(),
                               FilterNotUserRegCallBack())
    dp.callback_query.register(access_granted, F.data == 'access_granted', FilterDateBase())
