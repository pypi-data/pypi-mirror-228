"""Process the BLE data."""


import time
import logging

import dearpygui.dearpygui as dpg

from src.ble.scanning import ble_rs

from src.globals.helpers import ThreadWithReturnValue
from src.gps.scanning import process_gps


loggei = logging.getLogger(name=__name__)


def ble_data(company: bool) -> dict[str, str | int]:
    """Collate the da from the BLE API and return it."""
    loggei.debug(msg=f"{ble_data.__name__}()")

    target: tuple[str, str] = "dev", "rssi"

    # Grab the data from the API
    data = ble_rs(
        target=target[0]
    ) if not company else ble_rs(
        target=target[1]
    )

    loggei.info(msg=data)

    # If the data is empty, return an empty dict
    if not data:
        return {}

    # Grab the data from the dict
    if not company:
        # macs, rssi = (data.keys(), data.values())
        # print(f"RSSI {list(rssi)}")
        return data

    else:
        # macs, companies = (data.keys(), data.values())
        # print(f"Companies {list(companies)}")
        return data

    # return [
    #     list(macs),
    #     list(rssi)
    # ] if not company else [
    #     list(macs),
    #     list(companies)
    # ]


def threaded_ble_scan(company: bool) -> tuple[list, list]:
    """Scan for BLE signals and frequencies in a thread."""
    loggei.debug(msg=f"{threaded_ble_scan.__name__}()")

    dpg.configure_item(
        item="12",
        modal=True,
    )
    dpg.configure_item(
        item="ble_list",
        width=880,
        height=680,
    )

    dpg.add_text(
        tag="scan_text",
        default_value="SCANNING RSSI",
        pos=(400, 265)
    )

    ble_man = ThreadWithReturnValue(
        target=ble_data,
        args=(company[0],)
    )
    ble_man.start()

    ble_rssi = ThreadWithReturnValue(
        target=ble_data,
        args=(company[1],)
    )
    sleep_delay: float = 0.5

    count = 0

    while ble_man.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text",
            default_value="SCANNING RSSI" + "." * count
        )
        count = 0 if count > 3 else count
    count = 0

    ble_rssi.start()

    while ble_rssi.is_alive():
        time.sleep(sleep_delay)
        count += 1
        dpg.configure_item(
            item="scan_text",
            default_value="SCANNING MANUFACTURER" + "." * count
        )
        count = 0 if count > 3 else count
    ble_man: dict[str, str] = ble_man.join()
    ble_rssi: dict[str, int] = ble_rssi.join()

    ble_data_complete: dict[str, list[str, str, int]
                            ] = match_macs(base=ble_man, matcher=ble_rssi)

    dpg.delete_item(item="scan_text")

    dpg.configure_item(
        item="12",
        modal=False,
    )

    return ble_data_complete


def match_macs(
        base: dict[str, str], matcher: dict[str, int]
) -> dict[str, list[str, str, int]]:
    """Match the MAC addresses to the RSSI and manufacturer."""
    loggei.debug(msg=f"{match_macs.__name__}()")

    loggei.info(f"base: {len(base)}")
    loggei.info(f"matcher: {len(matcher)}")

    ble_return: dict[str, str] = {}

    # Create a set of the MAC addresses from base and matcher
    base_set = set(base.keys())
    matcher_set = set(matcher.keys())

    loggei.info(f"base_set: {base_set}")
    loggei.info(f"matcher_set: {matcher_set}")

    base_set = {mac.split(']')[1] for mac in base_set}

    loggei.info(f"base_set split: {base_set}")

    # Find the intersection of the two sets
    ble_intersection = base_set.intersection(matcher_set)

    loggei.info(f"ble_intersection: {ble_intersection}")

    gps_data: dict[str, str] = process_gps("lat_long")
    gps_data: str = gps_data.get("latitude") + gps_data.get("longitude")

    # Create a dict of the intersection
    for mac in ble_intersection:
        ble_return.update({mac: [matcher[mac][1].get("company")]})
        # print(f"matcher: {matcher[mac][4]}", end="\n\n")
        for key, value in base.items():
            if mac in key:
                ble_return[mac].append(value)
                ble_return[mac].append(matcher[mac][4].get("air_tag"))
                ble_return[mac].append(gps_data)

    loggei.info(f"ble_return: {ble_return}")

    return ble_return
