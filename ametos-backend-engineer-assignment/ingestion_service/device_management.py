from utils import Validator
from fastapi import HTTPException

class DeviceManager:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def is_device_registered(self, device_id: str) -> bool:
        """
        Checks if a device is registered in Redis cache.

        Args:
        device_id (str): The MAC address of the device to check.

        Returns:
        bool: True if the device is registered, False otherwise.
        """
        return self.redis_client.exists(device_id)

    def register_device(self, device_id: str, device_type: str) -> bool:
        """
        Registers a device and caches its details in Redis if the MAC address is valid.

        Args:
        device_id (str): The MAC address of the device.
        device_type (str): The type of the device.

        Returns:
        bool: True if registration was successful, False otherwise.

        Raises:
        HTTPException: If the MAC address format is invalid.
        """
        if not Validator.validate_mac_address(device_id):
            raise HTTPException(status_code=400, detail="Invalid MAC address format.")
        return self.redis_client.set(device_id, device_type)
