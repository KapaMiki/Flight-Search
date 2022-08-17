import aiofiles


class FlightService:

    @staticmethod
    async def get_flights() -> str:
        async with aiofiles.open('files/response_a.json') as f:
            data = await f.read()
            return data
