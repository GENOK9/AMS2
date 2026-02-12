from dataclasses import dataclass

@dataclass()
class Customer:
    """Kundendatenmodell"""
    firstName: str
    lastName: str
    country: str
    city: str
    street: str
    postalCode: int
    houseNumber: str
    gender: str = ""
    email: str = ""
    phoneNumber: str = ""
