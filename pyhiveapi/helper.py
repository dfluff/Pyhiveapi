
from .hive_data import Data


class Hive_Helper:

    def __init__():
        """intialise the helper class."""

    def get_device_name(n_id):
        """Resolve a id into a name"""
        try:
            product_name = Data.products[n_id]["state"]["name"]
        except KeyError:
            product_name = False

        try:
            device_name = Data.devices[n_id]["state"]["name"]
        except KeyError:
            device_name = False

        if product_name:
            return product_name
        elif device_name:
            return device_name
        elif n_id == "No_ID":
            return "Hive"
        else:
            return 'UNKNOWN'
