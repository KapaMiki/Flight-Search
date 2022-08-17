from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from apps.flights.views import flights_router
from apps.currency.services import CurrencyService


app = FastAPI(title='Airflow Service')

app.include_router(flights_router)


@app.on_event("startup")
@repeat_every(seconds=60*60*12)  # 12 hour
async def count_print() -> None:
    await CurrencyService.update_exchange_rate()
