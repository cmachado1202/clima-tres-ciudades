import asyncio
import json
import logging
import os
import tempfile
from pathlib import Path
import httpx
from ingestion.client import DataCollector

CITIES = {"Buenos Aires": (-34.6, -58.4), "Córdoba": (-31.4, -64.2), "Rosario": (-32.95, -60.64)}

async def main():
    async with httpx.AsyncClient(base_url="https://api.open-meteo.com", timeout=10) as session:
        collector = DataCollector(session)
        results = await asyncio.gather(*(collector.fetch(k, v) for k, v in CITIES.items()))
    valid = [record for record in results if record is not None]
    if valid:
        target = Path(__file__).resolve().parents[1] / "data" / "temperaturas.json"
        with tempfile.NamedTemporaryFile(mode="w", dir=target.parent, delete=False, encoding="utf-8") as out:
            json.dump(valid, out, indent=2, ensure_ascii=False)
        os.replace(out.name, target)
    logging.info("ciudades_recibidas=%s esperadas=%s", len(valid), len(CITIES))
    return int(len(valid) != len(CITIES))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    raise SystemExit(asyncio.run(main()))
