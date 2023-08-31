from src.helpers.helpers import NMEASerialReader, NMEASerialDecode
import json
import logging

logger = logging.getLogger(__name__)


def json_alt():
    """Returns a json object with the altitude from the NMEA serial reader."""
    logger.debug("json_alt function has been called")
    read = NMEASerialReader()
    decode = NMEASerialDecode()
    gpgga_nmea = read.read_all()
    alt = decode.decode_alt(gpgga_nmea) + "M"
    alt_value_pair = f"{alt}"
    logger.info(alt_value_pair)
    value = {"altitude": alt_value_pair}
    return json.dumps(value)
