"""Hive Sensor Module."""
from aiohttp import ClientSession
from typing import Optional
from .hive_data import Data
from .custom_logging import Logger
from .device_attributes import Attributes
from .hub import Hub
from .heating import Heating
from .hotwater import Hotwater
from .helper import Hive_Helper


class Sensor:
    """Hive Sensor Code."""

    def __init__(self, websession: Optional[ClientSession] = None):
        """Initialise."""
        self.log = Logger()
        self.attributes = Attributes()
        self.hub = Hub()
        self.heating = Heating(websession)
        self.hotwater = Hotwater(websession)
        self.type = "Sensor"

    async def get_sensor(self, device):
        await self.log.log(device["hive_id"], self.type, "Getting sensor data.")
        online = await self.attributes.online_offline(device['device_id'])

        dev_data = {}

        if online or "state" not in device:
            Hive_Helper.device_recovered(device['device_id'])

            dev_data = {"hive_id": device["hive_id"],
                        "hive_name": device["hive_name"],
                        "hive_type": device["hive_type"],
                        "ha_name": device["ha_name"],
                        "ha_type": device["ha_type"],
                        "device_id": device.get("device_id", None),
                        "device_name": device.get("device_name", None),
                        "hub_id": device.get("hub_id", None),
                        "device_data": {},
                        "custom": device.get("custom", None)
                        }

            data = {}
            if dev_data["device_id"] in Data.devices:
                data = Data.devices.get(device["device_id"], {})
            elif dev_data["hive_id"] in Data.products:
                data = Data.products.get(device["hive_id"], {})

            if dev_data["hive_type"] in Data.sensor_commands or dev_data.get("custom", None) in Data.sensor_commands:
                code = Data.sensor_commands.get(
                    dev_data["hive_type"], Data.sensor_commands.get(dev_data["custom"]))
                dev_data.update({"state": await eval(code),
                                 "device_data": data.get("props", None),
                                 "parent_device": data.get("parent", None)})
            elif device["hive_type"] in Data.HIVE_TYPES["Sensor"]:
                data = Data.devices.get(device["hive_id"], {})
                dev_data.update({"state": await self.get_state(device),
                                 "device_data": data.get("props", None),
                                 "parent_device": data.get("parent", None),
                                 "attributes": await self.attributes.state_attributes(device["hive_id"],
                                                                                      device["hive_type"])})

            await self.log.log(device["hive_id"], self.type,
                               "Device update {0}", info=Data.NODES[device["hive_id"]])
            Data.ha_devices.update({device['hive_id']: dev_data})
            return dev_data
        else:
            await self.log.error_check(device['device_id'], "ERROR", online)
            return device

    async def get_state(self, device):
        """Get sensor state."""
        await self.log.log(device["hive_id"], "Extra", "Getting state")
        state = None
        state = None
        final = None

        if device["hive_id"] in Data.products:
            data = Data.products[device["hive_id"]]
            if data["type"] == "contactsensor":
                state = data["props"]["status"]
            elif data["type"] == "motionsensor":
                state = data["props"]["motion"]["status"]
            final = Data.HIVETOHA[self.type].get(state, state)
            await self.log.log(device["hive_id"], "Extra", "Status is {0}", info=final)
            Data.NODES[device["hive_id"]]["State"] = final
        else:
            await self.log.error_check(device["hive_id"], "ERROR", "Failed")

        return final if final is None else Data.NODES[device["hive_id"]]["State"]

    async def online(self, device):
        """Get the online status of the Hive hub."""
        await self.log.log(device["hive_id"], "Extra", "Getting status")
        state = None
        final = None

        if device["hive_id"] in Data.devices:
            data = Data.devices[device["hive_id"]]
            state = data["props"]["online"]
            final = Data.HIVETOHA[self.type].get(state, state)
            await self.log.log(device["hive_id"], "Extra", "Status is {0}", info=final)
            Data.NODES[device["hive_id"]]["State"] = final
        else:
            await self.log.error_check(device["hive_id"], "ERROR", "Failed")

        return final if final is None else Data.NODES[device["hive_id"]]["State"]
