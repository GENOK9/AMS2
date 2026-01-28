from dataclasses import dataclass

@dataclass()
class Customer:
    """Kundendatenmodell"""
    firstname: str
    lastname: str
    country: str
    city: str
    street: str
    postal: int
    housenumber: str
    extra: str = ""
    email: str = ""
    phone: str = ""
