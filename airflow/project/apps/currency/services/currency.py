from datetime import datetime
from typing import Union
import json

import httpx

from config.extra import NATIONAL_BANK_KZ_BASE_URL, CURRENT_EXCHANGE_RATE_REDIS_KEY
from apps.utils.functions import send_get, convert_xml_to_dict, get_redis_client
from apps.utils.services import RedisCacheService


class CurrencyService:

    @staticmethod
    async def update_exchange_rate() -> None:
        exchange_rate_response = await CurrencyService.get_exchange_rate()
        xml_data = exchange_rate_response.content
        dict_data = convert_xml_to_dict(xml_data)
        data = {}

        for item in dict_data['rates']['generator']['item']:
            data[item['title']] = item['description']

        redis_client = await get_redis_client()
        await RedisCacheService.set_data(
            redis_client,
            CURRENT_EXCHANGE_RATE_REDIS_KEY,
            json.dumps(data)
        )

    @staticmethod
    async def get_exchange_rate(date=datetime.now().astimezone().strftime('%d.%m.%Y')):
        url = NATIONAL_BANK_KZ_BASE_URL + 'rss/get_rates.cfm'
        params = {
            'fdate': date
        }
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, params=params)
            return response
