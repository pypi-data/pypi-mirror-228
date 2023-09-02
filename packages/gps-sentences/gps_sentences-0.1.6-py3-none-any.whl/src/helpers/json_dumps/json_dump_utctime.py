from src.helpers.helpers import NMEASerialReader, NMEASerialDecode
import json
import logging

logger = logging.getLogger(__name__)


def json_utc_time():
    """Returns a json object with the UTC time from the Serial Reader."""
    logger.debug("json_utc_time function has been called")
    read = NMEASerialReader()
    decode = NMEASerialDecode()
    gpgga_nmea = read.read_all()
    utc_time = decode.decode_time(gpgga_nmea)
    time_value_pair = f"{utc_time} UTC"
    logging.info(time_value_pair)
    value = {"utc_time": time_value_pair}
    return json.dumps(value)
