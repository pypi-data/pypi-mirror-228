from typing import List
from . import auth

class WastePickup:
    """Class that represents a Waste pickup in the Borås Energi och Miljö API."""

    def __init__(self, raw_data: dict, auth: auth.Auth):
        """Initialize a waste pickup instance."""
        self.raw_data = raw_data
        self.auth = auth

    # Note: each property name maps the name in the returned data

    @property
    def containerId(self) -> int:
        """Return the ID (Kärl X) of the container."""
        return self.raw_data["WasteType"]

    @property
    def NextWastePickup(self) -> str:
        """Return the next pickup of the Waste container."""
        return self.raw_data["NextWastePickup"]

    @property
    def WastePickupsPerYear(self) -> int:
        """Return the number of pickups per year."""
        return self.raw_data["WastePickupsPerYear"]
    
    @property
    def WastePickupFrequency(self) -> str:
        """Return the frequency of the pickups."""
        return self.raw_data["WastePickupFrequency"]
    
    @property
    def ContainerType(self) -> int:
        """Return the type of the containers."""
        return self.raw_data["Designation"]
    
    @property
    def IsActive(self) -> bool:
        """Return the if the container delivery is active."""
        return self.raw_data["IsActive"]