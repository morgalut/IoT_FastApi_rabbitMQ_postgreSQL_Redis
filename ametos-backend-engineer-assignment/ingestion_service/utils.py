"""Utility module for the ingestion service.

This module provides utility functions such as validating specific data formats.
For example, it includes a Validator class for MAC address validation.
"""

import re

class Validator:
    """Utility class for validating data formats."""
    
    @staticmethod
    def validate_mac_address(mac: str) -> bool:
        """
        Validates that the provided string is a MAC address.

        Args:
            mac (str): The MAC address to validate.

        Returns:
            bool: True if the string is a valid MAC address, False otherwise.
        """
        return bool(re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac))

