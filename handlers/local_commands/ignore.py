import json
from typing import List

from lib.vkmini import VkApi
from utils import send_signal, find_mention_by_message
from settings import settings
from config import config


async def ignore_add(args: List[str], payload: str,
                     vk: VkApi, update: list) -> str:
    msg = (await vk('messages.getById', message_ids=update[1]))['items'][0]
    uid = await find_mention_by_message(msg, vk)
    if uid is None:
        return '⚠️ каво прости?7?'
    if uid == config.self_id:
        return 'ты что, с ума сошел??'
    uid = str(uid)
    if uid in settings.ignored_users:
        return '❔ он уже тут, ты о чём?7?'
    settings.ignored_users.append(uid)
    await settings.sync()
    return '✅ вот и ещё один дотик в игноре, ха!'


async def ignore_remove(args: List[str], payload: str,
                        vk: VkApi, update: list) -> str:
    msg = (await vk('messages.getById', message_ids=update[1]))['items'][0]
    uid = await find_mention_by_message(msg, vk)
    if uid is None:
        return '⚠️ прости, кто?'
    uid = str(uid)
    if uid not in settings.ignored_users:
        return '❔ эм... его нет в игноре, ты о чём?'
    settings.ignored_users.remove(uid)
    await settings.sync()
    return '✅ на первый раз прощаю, но потом...'


async def ignore_list(args: List[str], payload: str,
                      vk: VkApi, update: list) -> None:
    await send_signal(json.dumps({
            'access_key': config.access_key,
            'command': 'игнор',
            'message': (await vk('messages.getById',
                                 message_ids=update[1]))['items'][0],
            'chat': None
        },  ensure_ascii=False, separators=(',', ':'))
    )
