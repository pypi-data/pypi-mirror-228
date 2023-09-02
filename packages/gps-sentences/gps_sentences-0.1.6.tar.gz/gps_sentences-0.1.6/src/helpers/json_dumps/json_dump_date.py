from src.helpers.helpers import time_zone, local_time, date
import json
import logging

logger = logging.getLogger(__name__)


def json_date_time():
    """Returns the current date as a string in json format"""
    logger.debug("json_date_time function has been called")
    tz = time_zone()
    lt = local_time()
    day = date()
    date_value_pair = f"{day} {lt} {tz}"
    logger.info(date_value_pair)
    value = {"date_time": date_value_pair}
    return json.dumps(value)
