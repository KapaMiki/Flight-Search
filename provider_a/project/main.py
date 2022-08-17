import asyncio

from fastapi import FastAPI, Response

from services import FlightService


app = FastAPI(title='Provider A')


@app.get("/search/")
async def get_flights() -> Response:
    await asyncio.sleep(30)
    data = await FlightService.get_flights()
    return Response(data, media_type='application/json')
