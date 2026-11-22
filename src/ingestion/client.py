import asyncio
import logging
import httpx

log = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, session):
        self.session = session

    async def fetch(self, city, coordinates):
        lat, lon = coordinates
        params = {"latitude": lat, "longitude": lon, "current": "temperature_2m"}
        for attempt in range(2):
            try:
                response = await self.session.get("/v1/forecast", params=params)
                response.raise_for_status()
                return self.parse(city, response.json())
            except (httpx.HTTPError, KeyError, ValueError, TypeError) as error:
                transient = isinstance(error, httpx.TransportError) or (
                    isinstance(error, httpx.HTTPStatusError)
                    and (error.response.status_code >= 500 or error.response.status_code == 429)
                )
                log.error("ciudad=%s intento=%s error=%s", city, attempt + 1, error)
                if not transient or attempt == 1:
                    return None
                await asyncio.sleep(1)

    @staticmethod
    def parse(city, data):
        now = data["current"]
        return {"ciudad": city, "hora": now["time"], "temperatura": now["temperature_2m"],
                "unidad": data["current_units"]["temperature_2m"]}
