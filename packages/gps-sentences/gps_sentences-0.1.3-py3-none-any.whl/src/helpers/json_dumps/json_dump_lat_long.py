from src.helpers.helpers import NMEASerialReader, NMEASerialDecode
import json
import logging

logger = logging.getLogger(__name__)


def json_lat_long():
    """Returns the latitude and longitude of
    the current location in JSON format"""
    logger.debug("json_lat_long function has been called")
    read = NMEASerialReader()
    decode = NMEASerialDecode()
    gpgga_nmea = read.read_all()
    direction_lat = gpgga_nmea[3]
    direction_long = gpgga_nmea[5]
    lat = decode.decode_lat(gpgga_nmea)
    long = decode.decode_long(gpgga_nmea)
    lat_value_pair = f"{lat} {direction_lat}"
    long_value_pair = f"{long} {direction_long}"
    logging.info(lat_value_pair)
    logging.info(long_value_pair)
    values = {"latitude": lat_value_pair, "longitude": long_value_pair}
    return json.dumps(values)
