import json


class RedisCacheService:

    @staticmethod
    async def get_or_set_data(redis, key: str, value: dict):
        result = await RedisCacheService.get_data(redis, key)

        if not result:
            await RedisCacheService.set_data(redis, key, value)
            result = await RedisCacheService.get_data(redis, key)
        return result

    @staticmethod
    async def set_data(redis, key, value):
        await redis.set(
            key,
            value
        )

    @staticmethod
    async def get_data(redis, key):
        result = await redis.get(key)
        if result:
            return json.loads(result)
        return result
