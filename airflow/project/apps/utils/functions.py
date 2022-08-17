import requests
import xmltodict
import aioredis

from config.extra import REDIS_URL

def send_get(url, params=None, headers=None):
    return requests.get(url, params=params, headers=headers)


def convert_xml_to_dict(xml: str) -> dict:
    return xmltodict.parse(xml)


async def get_redis_client():
    return await aioredis.from_url(REDIS_URL)
