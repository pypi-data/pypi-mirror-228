import operator
import datetime
import time

from via import logger
from via.utils import (
    get_journeys,
    should_include_journey,
)
from via.models.journeys import Journeys
from via.db import db


GENERATING = []


def generate_geojson(
    transport_type: str,
    version: str = False,
    version_op: str = None,
    earliest_time: int = None,
    latest_time: int = None,
    place: str = None,
) -> dict:
    start = time.monotonic()

    logger.info(
        "Generating geojson: transport_type=%s version=%s version_op=%s earliest_time=%s latest_time=%s place=%s",
        transport_type,
        version,
        version_op,
        earliest_time,
        latest_time,
        place,
    )

    config = {
        "transport_type": "bike",
        "name": "bike",
        "version": version,
        "version_op": version_op if version else None,
        "earliest_time": earliest_time,
        "latest_time": latest_time,
        "place": place,
    }

    if config in GENERATING:
        logger.info("Already generating: %s", config)
        return

    GENERATING.append(config)

    try:
        logger.info('Generating geojson for "%s"', config["transport_type"])

        journeys = get_journeys(
            transport_type=config["transport_type"],
            earliest_time=earliest_time,
            latest_time=latest_time,
        )

        journeys = Journeys(
            data=[
                journey
                for journey in journeys
                if should_include_journey(
                    journey,
                    version_op=getattr(operator, version_op)
                    if version_op is not None
                    else None,
                    version=version,
                )
            ]
        )

        db.parsed_journeys.delete_many(
            {
                "journey_type": config["name"],
                "geojson_version": config["version"],
                "geojson_version_op": config["version_op"],
                "geojson_earliest_time": config["earliest_time"],
                "geojson_latest_time": config["latest_time"],
                "geojson_place": config["place"],
            }
        )

        data = None

        if len(journeys):
            data = journeys.geojson

            data["journey_type"] = config["name"]
            data["geojson_version"] = config["version"]
            data["geojson_version_op"] = config["version_op"]
            data["geojson_earliest_time"] = config["earliest_time"]
            data["geojson_latest_time"] = config["latest_time"]
            data["geojson_place"] = config["place"]
            data["save_time"] = datetime.datetime.utcnow().timestamp()

            db.parsed_journeys.insert_one(data)

    finally:
        GENERATING.remove(config)

    logger.info(
        "Generated geojson in %s seconds: transport_type=%s version=%s version_op=%s earliest_time=%s latest_time=%s place=%s",
        time.monotonic() - start,
        transport_type,
        version,
        version_op,
        earliest_time,
        latest_time,
        place,
    )

    return data
