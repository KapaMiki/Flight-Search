import asyncio
import json
from decimal import Decimal

import httpx

from apps.utils.const import FlightSearchStatusChoice, CurrencyCodeChoice
from apps.utils.services import RedisCacheService
from config.extra import PROVIDERS_FLIGHTS_URL, CURRENT_EXCHANGE_RATE_REDIS_KEY


class FlightSearchService:
    def __init__(self, search_id: str, redis_client):
        self.search_id = search_id
        self.redis_client = redis_client

    async def __set_flights_search(self, data):
        dumps_data = json.dumps({
            'search_id': self.search_id,
            'status': FlightSearchStatusChoice.PENDING.value,
            "items": data
        })
        result = await RedisCacheService.set_data(
            redis=self.redis_client,
            key=self.search_id,
            value=dumps_data)
        return result

    async def __update_or_set_flights_search(self, data):
        redis_result = await RedisCacheService.get_data(self.redis_client, self.search_id)
        if redis_result:
            # Append flights from another provider
            redis_result['items'] += data
            await RedisCacheService.set_data(
                redis=self.redis_client,
                key=self.search_id,
                value=json.dumps(redis_result)
            )
        else:
            # Save in cache flights
            await self.__set_flights_search(data)

    async def __change_search_status(self, status):
        redis_result = await RedisCacheService.get_data(self.redis_client, self.search_id)
        redis_result['status'] = status
        await RedisCacheService.set_data(
            redis=self.redis_client,
            key=self.search_id,
            value=json.dumps(redis_result)
        )

    async def get_data(self, client, url):
        response = await client.get(url)
        await self.__update_or_set_flights_search(response.json())

    async def search_flights_from_providers(self):
        await self.__set_flights_search(data=[])

        async with httpx.AsyncClient(timeout=None) as client:
            tasks = [self.get_data(client, url) for url in PROVIDERS_FLIGHTS_URL]
            await asyncio.gather(*tasks)

            # After data collection, change the status to completed
            await self.__change_search_status(FlightSearchStatusChoice.COMPLETED.value)

            # Close redis connection
            await self.redis_client.close()

    async def get_flights_by_search_id(self, currency):
        result = await RedisCacheService.get_data(self.redis_client, self.search_id)
        await self.__convert_flights_to_target_currency(result['items'], currency)
        await self.__sort_flights_by_price(result['items'])
        return result

    async def __convert_flights_to_target_currency(self, flights: list, target_currency: str) -> None:
        """ IN developing """
        pass

    async def __sort_flights_by_price(self, flights: list) -> None:
        """ IN developing """
        pass
