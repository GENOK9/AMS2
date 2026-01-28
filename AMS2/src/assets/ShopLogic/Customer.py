from dataclasses import dataclass

@dataclass()
class Customer:
    """Kundendatenmodell"""
    firstname: str
    lastname: str
    city: str
    street: str
    postal: int
    housenumber: str
    extra: str = ""
    gender: str = ""
    email: str = ""
    phone: str = ""

    def get_full_address(self) -> str:
        """Vollständige Adresse formatiert"""
        return f"{self.street} {self.housenumber}{self.extra}, {self.postal} {self.city}"

    def get_full_name(self) -> str:
        """Vollständiger Name"""
        return f"{self.firstname} {self.lastname}"