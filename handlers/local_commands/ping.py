from typing import List
import time

from lib.vkmini import VkApi
from utils import get_plural


pings = {
    'пинг': 'n2g:ПОНГ',
    'кинг': 'n2g:КОНГ',
    'пиу': 'n2g:ПАУ',
    'пинг': 'n2g:ПОНГ',
}


async def ping(args: List[str], payload: str, vk: VkApi, update: list) -> str:
    latency = round(time.time() - update[4], 1)
    if latency < 0:
        latency = "(я хз чтослучилось, давай ещё раз)"
    else:
        latency = f"Задержка ≈{str(latency)} секунд{get_plural(latency, 'а', 'ы', '', 'ы')}"  # noqa
    resp = pings.get(update[5], 'че?')
    return f"{resp} (Н_LP мод)\n{latency}"
