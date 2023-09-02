""" a helpers file to provide functions to the main program """

import serial
import logging
import pathlib
import time
import datetime
import platform
import subprocess


""" used to establish logging file and path to the log file """
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: %(name)s :: %(message)s :: %(levelname)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename=f"{ROOT}/gps_sentences.log",
    filemode="w",
)

""" initialize logger """
logger = logging.getLogger(name=__name__)

""" Find the correct GPS device path and serial number if necessary """


def device_names() -> list[str]:
    """Use a bash script to list connected microarchitectures."""
    if platform.system().lower != "windows":
        # Avoid crashing program if there are no devices detected
        try:
            listing_script = [
                # f'#!/bin/bash\n'
                f"for sysdevpath in $(find /sys/bus/usb/devices/usb*/ "
                f'-name dev | grep "ACM"); do\n'
                f'(syspath={"${sysdevpath%/dev}"}\n'
                f'devname={"$(udevadm info -q name -p $syspath)"}\n'
                f'[[ {"$devname"} == "bus/"* ]] && exit\n'
                f'eval "$(udevadm info -q property --export -p $syspath)"\n'
                f'[[ -z "$ID_SERIAL" ]] && exit\n'
                f'echo "/dev/$devname - $ID_SERIAL"\n'
                f") done"
            ]
            devices: subprocess.CompletedProcess[str] = subprocess.run(
                args=listing_script,
                shell=True,
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                capture_output=False,
                check=True,
            )
        except TypeError:
            logger.warning(msg=f"No devices detected | {device_names.__name__}")
            devices = subprocess.CompletedProcess(
                args="",
                returncode=1,
                stdout="",
                stderr="",
            )

    _devices: list = list(
        devices.stdout.strip().split(sep="\n"))  # type: ignore

    logger.info(msg=f"Devices found: {_devices} | {device_names.__name__}")

    # If there is only one device skip the hooplah
    if len(_devices) == 1:
        return _devices
    return sorted(_devices)


DEVICE: list[str] = device_names()


def return_device_info(
    device_list: list[str] = DEVICE,
    device_to_find: str = "GPS",
    path_to_find: str = "dev",
) -> dict[str, str] | str:
    """Return the device path and serial of the name Teensy."""
    teensy_info: dict[str, str] = {}

    # Initial process the device names
    devices = [device.split(sep="_") for device in device_list]

    # filter and return only specified devices

    desired_device = [i for i in devices if device_to_find in i]
    if not len(desired_device):
        logger.error(
            """Device not found. Ensure your GPS 
            device is plugged into the serial port."""
        )
        logger.error(
            """Index Error has been triggered. No GPS device is plugged in 
            or the device is not being detected from the serial port."""
        )
        exit()
    else:
        intended_device_path = desired_device[0]
        path = intended_device_path[0]
        path_try = path.split(sep="-")[0]
        path_corrected = path_try[:-1]
        path_type_corrected = str(path_corrected)
        logger.info(path_type_corrected)
        logger.debug("GPS device information has been found.")

    # Create the dictionary of the Teensy path and serial number
    for _i, val in enumerate(desired_device):
        teensy_info[val[-1]] = val[0].split(sep="-")[0]

    # if teensy_info == {}:
    #     loggey.error(msg="No Teensy device found")
    #     return {"0": "0"}

    return teensy_info if device_to_find != "GPS" else path_type_corrected


"""Creation of the variable that is used to store the path to the GPS device"""
corret_path = return_device_info()


def time_zone() -> str:
    """Creation of the method that is used to display the time zone."""
    logger.debug("Displaying time zone function is in use")
    y = time.tzname
    logger.info(y[0])
    return y[0]


def local_time() -> str:
    """Creation of the method that is used to display the local time."""

    logger.debug("Displaying local time function is in use")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    logger.info(current_time)
    return current_time


def date() -> str:
    """Creation of the method that is used to display the date."""
    logger.debug("Displaying date function is in use")
    today = datetime.date.today()
    logger.info(today)
    return today.strftime("%d-%b-%y")


class NMEASerialReader:
    """Creation of the class and class variable that is
    used to read the serial data from the serial port."""

    _port_info_corrected = corret_path
    logger.info(_port_info_corrected)
    logger.debug("Serial reader class has been called")

    def __init__(self) -> None:
        """Creation of the constructor that
        is used to initialize the serial port."""
        self.ser = serial.Serial(
            str(NMEASerialReader._port_info_corrected), baudrate=9600, timeout=5
        )

    @classmethod
    def change_to_list(cls, string: str) -> list:
        """Creation of the classmethod that is used to later convert a
        string to a list for later implementation with
        spaces being the delimitter."""

        logger.debug("Conversion to string function is in use")
        li = list(string.split(","))
        logger.info(li)
        return li

    @classmethod
    def read_all(cls) -> list:
        """Creation of the classmethod that is used
        to read all the data from the serial port."""
        logger.debug("Read all function is in use")
        ser = serial.Serial(
            f"{NMEASerialReader._port_info_corrected}", baudrate=9600, timeout=5
        )
        # read all the data from the serial port and store it in a list of strings
        data = ser.readline()
        store = []
        while True:
            data_type_corrected = str(data)
            data_corrected = data_type_corrected[2:-5]
            data = ser.readline()
            if data_corrected.split(",")[0] == "$GPGGA":
                store.append(str(data_corrected))
                store_type_corrected = str(store)
                store_corrected = store_type_corrected[2:-2]
                store_list = NMEASerialReader.change_to_list(store_corrected)
                logger.info(store_corrected)
                break
        return store_list


class NMEASerialDecode(NMEASerialReader):
    def __init__(self) -> None:
        """Creation of the constructor that is
        used to initialize the decoding of the serial port."""
        self.ser = serial.Serial(
            str(NMEASerialReader._port_info_corrected), baudrate=9600, timeout=5
        )
        logger.debug("Serial decode class has been called")

    @classmethod
    def slice_time(cls, utc_time: str) -> str:
        """Creation of the classmethod that is used
        to properly format the UTC time from the serial port."""
        logger.debug("Slicing time function is in use")
        string = str(utc_time)
        time1 = string[0:2]
        time2 = string[2:4]
        time3 = string[4:6]
        joined_time = f"{time1}:{time2}:{time3}"
        logger.info(joined_time)
        return joined_time

    @classmethod
    def lat_conversion(cls, lat_value: str) -> float:
        """Creation of the classmethod that is used
        to properly convert the latitude from the serial port."""
        logger.debug("Conversion to lat dec degrees float function is in use")
        try:
            lat_value = str(lat_value)
            first_two_digits = lat_value[0:2]
            remainder = lat_value[2:]
            deg = float(first_two_digits)
            min = float(remainder)
            decDegrees = float(deg) + float(min / 60)
            decDegrees_rounded = round(decDegrees, 6)
            logger.info(decDegrees_rounded)
            return decDegrees_rounded
        except ValueError:
            logger.error("Latitude value is not found")
            return 0

    @classmethod
    def long_conversion(cls, long_value: str) -> float:
        """Creation of the classmethod that is used to
        properly convert the longitude from the serial port."""
        logger.debug("Conversion to long dec degrees float function is in use")
        try:
            long_value = str(long_value)
            first_three_digits = long_value[0:3]
            remainder = long_value[3:]
            deg = float(first_three_digits)
            min = float(remainder)
            decDegrees = float(deg) + float(min / 60)
            decDegrees_rounded = round(decDegrees, 6)
            logger.info(decDegrees_rounded)
            return decDegrees_rounded
        except ValueError:
            logger.error("Longitude value is not found")
            return 0

    @classmethod
    def decode_time(cls, nmea_list_sentence: list) -> str:
        """Creation of the classmethod that is used to
        decode the time from the NMEA sentences from the serial port."""

        logger.debug("Decoding time function is in use")
        time = nmea_list_sentence[1]
        time_type_corrected = str(time)
        time_formatted = time_type_corrected[:-3]
        time_formatted = NMEASerialDecode.slice_time(time_formatted)
        logger.info(time_formatted)
        return time_formatted

    @classmethod
    def decode_alt(cls, nmea_list_sentence: list) -> str:
        """Creation of the classmethod that is used to decode
        the altitude from the NMEA sentences from the serial port."""

        logger.debug("Decoding alt function is in use")
        alt = nmea_list_sentence[9]
        alt_type_corrected = str(alt)
        logger.info(alt_type_corrected)
        return alt_type_corrected

    @classmethod
    def decode_lat(cls, nmea_list_sentence: list) -> float:
        """Creation of the classmethod that is used
        to decode the latitude from the NMEA sentences from the serial port."""

        logger.debug("Decoding lat function is in use")
        lat = nmea_list_sentence[2]
        lat_type_corrected = str(lat)
        final_lat_value = NMEASerialDecode.lat_conversion(lat_type_corrected)
        logger.info(final_lat_value)
        return final_lat_value

    @classmethod
    def decode_long(cls, nmea_list_sentence: list) -> float:
        """Creation of the classmethod that is used to decode
        the longitude from the NMEA sentences from the serial port."""

        logger.debug("Decoding long function is in use")
        long = nmea_list_sentence[4]
        long_type_corrected = str(long)
        final_long_value = NMEASerialDecode.long_conversion(long_type_corrected)
        logger.info(final_long_value)
        return final_long_value
