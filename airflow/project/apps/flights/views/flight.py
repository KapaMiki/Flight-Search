import uuid

from fastapi import APIRouter
from fastapi import BackgroundTasks

from apps.flights.services import FlightSearchService
from apps.utils.services import RedisCacheService
from apps.utils.functions import get_redis_client


flights_router = APIRouter(prefix='/search')


@flights_router.get("/")
async def get_flights(background_tasks: BackgroundTasks):
    search_id = str(uuid.uuid4())
    redis_client = await get_redis_client()
    search_service = FlightSearchService(search_id, redis_client)
    background_tasks.add_task(search_service.search_flights_from_providers)
    return {'search_id': search_id}


@flights_router.get("/{search_id}/{currency}/")
async def get_flights_by_search_id(search_id: str, currency: str):
    redis_client = await get_redis_client()
    # result = await RedisCacheService.get_data(redis_client, search_id)
    search_service = FlightSearchService(search_id, redis_client)
    data = await search_service.get_flights_by_search_id(currency)
    await redis_client.close()
    return data
