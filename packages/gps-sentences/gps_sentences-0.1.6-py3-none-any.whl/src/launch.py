""" Create a package that will read and decode GPS sentences."""
from .helpers.serial_run import serial_reader
from .helpers.serial_run import time_information
from .helpers.json_dumps.json_dump_lat_long import json_lat_long
from .helpers.json_dumps.json_dump_alt import json_alt
from .helpers.json_dumps.json_dump_utctime import json_utc_time
from .helpers.json_dumps.json_dump_date import json_date_time
from fastapi import FastAPI
import uvicorn
import logging
import pathlib
import logging.config


# Initialize the logger
logger = logging.getLogger(name=__name__)

# Log file path
ROOT = pathlib.Path(__file__).parent.parent.absolute()
log_config = ROOT / "src" / "logging.conf"
log_file_path = ROOT / "gps_sentences.log"

# Configure the logger
logging.config.fileConfig(
    fname = f"{log_config}",
    disable_existing_loggers=False,
    defaults={"gps_sentences.log": f"{log_file_path}"},
)


def main():
    """Main function"""
    serial_reader(time_information())
    logger.debug("Main serial reader function has been called.")
    app = FastAPI()
    logger.debug("FastAPI app has been initialized.")

    @app.get("/")
    async def index():
        """Root endpoint"""
        logger.debug("Root endpoint has been called.")
        return {"message": "This is the root endpoint."}

    @app.get("/all_serial_data")
    async def all_serial_data():
        """Returns all serial data"""
        logger.debug("All serial data endpoint has been called.")
        return {serial_reader(time_information())}

    @app.get("/all_serial_data/lat_long")
    async def all_serial_data_lat_long():
        """Returns the latitude and longitude of the
        current location in JSON format"""
        logger.debug("Latitude and longitude endpoint has been called.")
        return {json_lat_long()}

    @app.get("/all_serial_data/altitude")
    async def all_serial_data_altitude():
        """Returns the altitude of the current location in JSON format"""
        logger.debug("Altitude endpoint has been called.")
        return {json_alt()}

    @app.get("/all_serial_data/utc_time")
    async def all_serial_data_utc_time():
        """Returns the UTC time of the current location in JSON format"""
        logger.debug("UTC time endpoint has been called.")
        return {json_utc_time()}

    @app.get("/all_serial_data/date_time")
    async def all_serial_data_date_time():
        """Returns the date and time of the current location in JSON format"""
        logger.debug("Date and time endpoint has been called.")
        return {json_date_time()}

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8085,
        log_level="debug",
        log_config=str(log_config),
        use_colors=True,
    )
    logger.debug("Uvicorn has been called.")


if __name__ == "__main__":
    """Main function"""
    main()
    logger.debug("Main function has been called.")
